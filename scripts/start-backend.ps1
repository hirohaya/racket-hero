# Script para inicializar o backend em novo terminal
# Abre em foreground (não em background)

$backendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend"

# Abrir novo terminal PowerShell com o backend
Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location '$backendPath'; Write-Host '[BACKEND] FastAPI iniciando...' -ForegroundColor Cyan; python main.py`"" -WindowStyle Normal

Write-Host "[OK] Backend aberto em novo terminal!" -ForegroundColor Green
Write-Host "Acesso:" -ForegroundColor Cyan
Write-Host "  API:  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
