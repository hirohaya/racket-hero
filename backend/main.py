# main.py - Aplicação FastAPI principal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from database import init_db
from routers import auth

# Criar aplicação FastAPI
app = FastAPI(
    title="Racket Hero API",
    description="API para gerenciamento de eventos de tênis de mesa",
    version="1.0.0"
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

# Evento de startup
@app.on_event("startup")
def startup():
    """
    Inicializar banco de dados quando aplicação inicia.
    Cria todas as tabelas definidas nos modelos.
    """
    print("[INFO] Inicializando banco de dados...")
    init_db()
    print("[INFO] Banco de dados pronto!")

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
