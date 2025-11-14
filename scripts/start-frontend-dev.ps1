# Script para inicializar o frontend em modo desenvolvimento em novo terminal
# Abre em foreground (não em background)

$frontendPath = "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\frontend"

# Abrir novo terminal PowerShell com o frontend
Start-Process powershell -ArgumentList "-NoExit -Command `"Set-Location '$frontendPath'; Write-Host '[FRONTEND] React iniciando...' -ForegroundColor Yellow; npm start`"" -WindowStyle Normal

Write-Host "[OK] Frontend aberto em novo terminal!" -ForegroundColor Green
Write-Host "Acesso:" -ForegroundColor Yellow
Write-Host "  App: http://localhost:3000" -ForegroundColor Yellow
Write-Host "  Debug: http://localhost:3000/debug" -ForegroundColor Yellow
