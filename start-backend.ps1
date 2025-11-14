# Script para inicializar o backend

Write-Host "🚀 Iniciando Backend Racket Hero..." -ForegroundColor Green
Write-Host "API: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan

Set-Location "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend"

# Executar servidor
python main.py
