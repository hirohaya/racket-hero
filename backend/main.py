# main.py - Aplicação FastAPI principal

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import os
from pathlib import Path
import logging
import atexit

from database import init_db, get_db, engine
from routers import auth, events, players, matches, ranking, evento_organizadores, admin, seed
from logger_production import setup_logging, get_logger
from backup_manager import backup_endpoint_handler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Configurar logging production
setup_logging(log_level=logging.INFO, log_dir='logs', json_format=True)
log = get_logger("main")

# Force rebuild timestamp
print("[DEPLOY] 2025-01-09 13:46 - Racket Hero app started with all UI improvements")

# Inicializar banco de dados na importação
try:
    init_db()
    log.info("Banco de dados inicializado")
except Exception as e:
    log.error(f"Erro ao inicializar banco de dados: {e}", exc_info=True)

# Criar aplicação FastAPI
app = FastAPI(
    title="Racket Hero API",
    description="API para gerenciamento de eventos de tênis de mesa",
    version="1.0.0"
)

# Middleware de CORS
try:
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:3000,http://localhost:8000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    log.info(f"CORS configurado para: {CORS_ORIGINS}")
except Exception as e:
    log.error(f"Erro ao configurar CORS: {e}")

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Verificar saúde da API"""
    return {
        "status": "ok",
        "message": "Racket Hero API is running",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Database health check endpoint
@app.get("/health/db", tags=["System"])
async def health_check_db(db: Session = Depends(get_db)):
    """Verificar saúde da API e do banco de dados"""
    try:
        # Testar conexão com o banco
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "ok"
        db_message = "Database connection successful"
    except Exception as e:
        db_status = "error"
        db_message = f"Database connection failed: {str(e)}"
        log.error(f"Health check DB error: {e}", exc_info=True)

# Endpoint para criar tabelas (para debug/setup)
@app.post("/admin/create-tables", tags=["Admin"])
async def create_tables():
    """Criar tabelas no banco de dados (ADMIN ONLY - para setup)"""
    try:
        from database import Base
        Base.metadata.create_all(bind=engine)
        
        # Verificar quais tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        log.info(f"Tabelas criadas: {tables}")
        
        return {
            "status": "success",
            "message": f"Tabelas criadas com sucesso",
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        log.error(f"Erro ao criar tabelas: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Erro ao criar tabelas: {str(e)}"
        }

# Endpoint para seed de dados de teste
@app.post("/admin/seed-test-data", tags=["Admin"])
async def seed_test_data(db: Session = Depends(get_db)):
    """Adicionar contas de teste ao banco de dados (ADMIN ONLY)"""
    try:
        from models.usuario import Usuario, TipoUsuario
        from models.event import Event
        from models.player import Player
        from models.evento_organizador import EventoOrganizador
        from utils.security import hash_password
        
        log.info("[SEED] Iniciando seed de dados de teste...")
        
        # Verificar se já existe organizador
        organizador = db.query(Usuario).filter(
            Usuario.email == "organizador@test.com"
        ).first()
        
        if not organizador:
            log.info("[SEED] Criando usuário ORGANIZADOR...")
            organizador = Usuario(
                email="organizador@test.com",
                nome="Organizador Teste",
                senha_hash=hash_password("Senha123!"),
                tipo=TipoUsuario.ORGANIZADOR,
                ativo=True
            )
            db.add(organizador)
            db.flush()
            log.info("[SEED] ✓ Organizador criado")
        else:
            log.info("[SEED] Organizador já existe")
        
        # Criar evento de teste
        evento = db.query(Event).filter(Event.name == "Torneio Teste").first()
        if not evento:
            log.info("[SEED] Criando evento TORNEIO TESTE...")
            evento = Event(
                name="Torneio Teste",
                date="2025-12-01",
                time="14:00",
                active=True,
                usuario_id=organizador.id
            )
            db.add(evento)
            db.flush()
            log.info("[SEED] ✓ Evento criado")
        else:
            log.info("[SEED] Evento já existe")
        
        # Vincular organizador ao evento
        if evento and organizador:
            org_link = db.query(EventoOrganizador).filter(
                EventoOrganizador.event_id == evento.id,
                EventoOrganizador.usuario_id == organizador.id
            ).first()
            
            if not org_link:
                log.info("[SEED] Vinculando organizador ao evento...")
                org_link = EventoOrganizador(
                    event_id=evento.id,
                    usuario_id=organizador.id,
                    é_criador=1
                )
                db.add(org_link)
                db.flush()
                log.info("[SEED] ✓ Organizador vinculado")
        
        # Criar usuários jogadores
        test_accounts = [
            ("Jogador Teste", "jogador@test.com"),
            ("João Silva", "joao.silva@example.com"),
            ("Maria Santos", "maria.santos@example.com"),
            ("Pedro Oliveira", "pedro.oliveira@example.com"),
            ("Ana Costa", "ana.costa@example.com"),
            ("Lucas Ferreira", "lucas.ferreira@example.com"),
            ("Patricia Alves", "patricia.alves@example.com"),
            ("Roberto Gomes", "roberto.gomes@example.com"),
            ("Juliana Rocha", "juliana.rocha@example.com"),
            ("Bruno Martins", "bruno.martins@example.com"),
            ("Camila Ribeiro", "camila.ribeiro@example.com"),
        ]
        
        created_users = []
        log.info(f"[SEED] Criando {len(test_accounts)} usuários jogadores...")
        
        for nome, email in test_accounts:
            existing_user = db.query(Usuario).filter(Usuario.email == email).first()
            if not existing_user:
                new_user = Usuario(
                    email=email,
                    nome=nome,
                    senha_hash=hash_password("Senha123!"),
                    tipo=TipoUsuario.JOGADOR,
                    ativo=True
                )
                db.add(new_user)
                db.flush()
                created_users.append(nome)
                log.info(f"[SEED] ✓ {nome}")
            else:
                log.info(f"[SEED] {nome} já existe")
        
        # Adicionar jogadores ao evento
        if evento:
            log.info("[SEED] Adicionando jogadores ao evento...")
            for nome, email in test_accounts:
                user = db.query(Usuario).filter(Usuario.email == email).first()
                existing_player = db.query(Player).filter(
                    Player.event_id == evento.id,
                    Player.name == nome
                ).first()
                
                if not existing_player and user:
                    player = Player(
                        usuario_id=user.id,
                        event_id=evento.id,
                        name=nome,
                        initial_elo=1600
                    )
                    db.add(player)
                    db.flush()
                    log.info(f"[SEED] ✓ {nome} adicionado ao evento")
        
        db.commit()
        
        log.info("[SEED] Seed concluído com sucesso!")
        
        return {
            "status": "success",
            "message": "Dados de teste inseridos com sucesso",
            "created_users": created_users,
            "total_users": len(test_accounts),
            "event": {
                "id": evento.id,
                "name": evento.name,
                "date": evento.date
            }
        }
    except Exception as e:
        db.rollback()
        log.error(f"[SEED] Erro ao seed: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Erro ao adicionar dados de teste: {str(e)}"
        }
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "api": {
            "status": "ok",
            "version": "1.0.0"
        },
        "database": {
            "status": db_status,
            "message": db_message
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Incluir routers (ANTES das rotas estáticas)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(evento_organizadores.router)  # Já tem prefix /events
app.include_router(players.router, prefix="/api/players", tags=["Players"])
app.include_router(matches.router, prefix="/api/matches", tags=["Matches"])
app.include_router(ranking.router, prefix="/api/ranking", tags=["Ranking"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(seed.router, tags=["Development"])

# Agendar backups diários (3 da manhã)
scheduler = BackgroundScheduler()
scheduler.add_job(
    backup_endpoint_handler,
    trigger=CronTrigger(hour=3, minute=0),
    id='daily_backup',
    name='Daily database backup',
    replace_existing=True
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
log.info("[OK] Agendador de backup iniciado (3:00 AM diariamente)")

# Servir aplicação React (build) - DEPOIS das rotas de API
frontend_build_path = Path(__file__).parent.parent / "frontend" / "build"
index_file = frontend_build_path / "index.html"

@app.get("/", include_in_schema=False)
async def serve_index():
    """Servir o arquivo index.html da build do React"""
    if index_file.exists():
        return FileResponse(index_file)
    return {"error": "Frontend build not found"}

@app.get("/{path:path}", include_in_schema=False)
async def serve_static(path: str):
    """Servir arquivos estáticos do frontend"""
    # NÃO servir rotas /api - deixar FastAPI lidar com elas
    if path.startswith("api") or path.startswith("api/"):
        # Deixar o FastAPI retornar 404 padrão para /api routes não encontradas
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "Not found"}, status_code=404)
    
    file_path = frontend_build_path / path
    
    # Se é um arquivo estático, servir
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    # Se é uma rota do React, servir index.html
    if index_file.exists():
        return FileResponse(index_file)
    
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    
    # Executar servidor
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,  # Auto-reload desativado para produção
        log_level="info"
    )
