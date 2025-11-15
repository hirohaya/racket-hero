# main.py - Aplicação FastAPI principal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager

from database import init_db
from routers import auth, events, players, matches, ranking
from logger import get_logger

log = get_logger("main")

# Lifespan para startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar startup e shutdown da aplicação"""
    # Startup
    log.info("Inicializando banco de dados...")
    init_db()
    log.info("Banco de dados pronto!")
    
    yield
    
    # Shutdown
    log.info("Encerrando aplicação...")

# Criar aplicação FastAPI
app = FastAPI(
    title="Racket Hero API",
    description="API para gerenciamento de eventos de tênis de mesa",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware de CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Verificar saúde da API"""
    return {
        "status": "ok",
        "message": "Racket Hero API is running",
        "version": "1.0.0"
    }

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])
app.include_router(ranking.router, prefix="/ranking", tags=["Ranking"])

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
