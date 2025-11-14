# Script para inicializar Backend e Frontend em terminais separados
# Cada um roda em foreground (não em background)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  [RACKET HERO] Inicializador" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend"
$frontendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\frontend"

# Verificar se servidores já estão rodando
Write-Host "[*] Verificando se servidores já estão rodando..." -ForegroundColor Yellow

$backendRunning = netstat -ano 2>$null | Select-String "8000.*LISTENING"
$frontendRunning = netstat -ano 2>$null | Select-String "3000.*LISTENING"

if ($backendRunning) {
    Write-Host "[AVISO] Backend já está rodando na porta 8000!" -ForegroundColor Red
} else {
    Write-Host "[+] Iniciando Backend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location '$backendPath'; Write-Host '[BACKEND] FastAPI iniciando...' -ForegroundColor Cyan; python main.py`"" -WindowStyle Normal
    Start-Sleep -Seconds 1
}

if ($frontendRunning) {
    Write-Host "[AVISO] Frontend já está rodando na porta 3000!" -ForegroundColor Red
} else {
    Write-Host "[+] Iniciando Frontend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location '$frontendPath'; Write-Host '[FRONTEND] React iniciando...' -ForegroundColor Yellow; npm start`"" -WindowStyle Normal
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "[OK] SERVIDORES INICIADOS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Backend:  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "[*] Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "[*] Debug:    http://localhost:3000/debug" -ForegroundColor Yellow
Write-Host ""
