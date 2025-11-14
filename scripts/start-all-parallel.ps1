#!/usr/bin/env pwsh
# Script para inicializar Backend e Frontend em paralelo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[RACKET HERO] Inicializador" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend"
$frontendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\frontend"

# Iniciar Backend como job
Write-Host "[+] Iniciando Backend..." -ForegroundColor Green
$backendJob = Start-Job -Name "RacketHero-Backend" -ScriptBlock {
    Set-Location $using:backendPath
    Write-Host "[BACKEND] FastAPI iniciando..." -ForegroundColor Green
    Write-Host "[BACKEND] http://127.0.0.1:8000" -ForegroundColor Cyan
    python main.py
}

# Aguardar 3 segundos
Write-Host "[*] Aguardando 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host ""

# Iniciar Frontend como job
Write-Host "[+] Iniciando Frontend..." -ForegroundColor Green
$frontendJob = Start-Job -Name "RacketHero-Frontend" -ScriptBlock {
    Set-Location $using:frontendPath
    Write-Host "[FRONTEND] React iniciando..." -ForegroundColor Green
    Write-Host "[FRONTEND] http://localhost:3000" -ForegroundColor Cyan
    npm start
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "[OK] SERVIDORES INICIADOS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Backend:  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "[*] Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "[*] Docs:     http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos:" -ForegroundColor Yellow
Write-Host "  Get-Job" -ForegroundColor Gray
Write-Host "  Receive-Job -Name RacketHero-Backend -Keep" -ForegroundColor Gray
Write-Host "  Stop-Job -Name RacketHero-*" -ForegroundColor Gray
Write-Host ""
