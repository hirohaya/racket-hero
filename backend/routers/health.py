# routers/health.py - Health check endpoints

from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
    """Verificar saúde da API"""
    return {
        "status": "ok",
        "message": "Racket Hero API is running",
        "version": "1.0.0"
    }
