#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script para inicializar Backend e Frontend do Racket Hero simultaneamente
    
.DESCRIPTION
    Este script inicia:
    - Backend FastAPI na porta 8000
    - Frontend React na porta 3000
    
    Ambos rodam em janelas/abas separadas do terminal
    
.EXAMPLE
    .\start-all.ps1
#>

Write-Host "
╔════════════════════════════════════════════════════════════╗
║           🏓 RACKET HERO - Inicializador                   ║
╚════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

$backendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend"
$frontendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\frontend"

# Verificar se os diretórios existem
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Pasta backend não encontrada: $backendPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ Pasta frontend não encontrada: $frontendPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Pastas encontradas" -ForegroundColor Green
Write-Host ""

# Iniciar Backend em novo terminal
Write-Host "🚀 Iniciando Backend..." -ForegroundColor Yellow
$backendScript = @"
Write-Host "🚀 Backend Racket Hero" -ForegroundColor Green
Write-Host "API: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Set-Location "$backendPath"
python main.py
"@

Start-Process pwsh -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal

Write-Host "✅ Backend iniciado em novo terminal" -ForegroundColor Green
Write-Host ""

# Aguardar um pouco para o backend iniciar
Write-Host "⏳ Aguardando 5 segundos para o backend iniciar..." -ForegroundColor Yellow
for ($i = 5; $i -gt 0; $i--) {
    Write-Host "`r⏳ Aguardando $i segundos..." -NoNewline
}
Write-Host ""

# Iniciar Frontend em novo terminal
Write-Host "🚀 Iniciando Frontend..." -ForegroundColor Yellow
$frontendScript = @"
Write-Host "🚀 Frontend Racket Hero" -ForegroundColor Green
Write-Host "App: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Set-Location "$frontendPath"
npm start
"@

Start-Process pwsh -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal

Write-Host "✅ Frontend iniciado em novo terminal" -ForegroundColor Green
Write-Host ""

Write-Host "
╔════════════════════════════════════════════════════════════╗
║                   ✅ TUDO PRONTO!                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  📍 Backend:  http://127.0.0.1:8000                        ║
║  📍 Frontend: http://localhost:3000                        ║
║  📍 Docs:     http://127.0.0.1:8000/docs                  ║
║                                                            ║
║  💡 Dica: Ambos os servidores abriram em abas novas       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
" -ForegroundColor Green

Write-Host "🔄 Script principal aguardando... (Ctrl+C para encerrar)" -ForegroundColor Cyan
Read-Host "Pressione ENTER para continuar"
