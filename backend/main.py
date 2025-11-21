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
