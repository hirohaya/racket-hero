# Script para inicializar o frontend
# Uso: .\start-frontend.ps1

Write-Host "🚀 Inicializando Frontend Racket Hero..." -ForegroundColor Green

# Ir para pasta frontend
Set-Location "C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\frontend"

# Verificar se node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Instalando dependências..." -ForegroundColor Yellow
    npm install
}

Write-Host "🔨 Compilando React..." -ForegroundColor Yellow
npm run build

if (Test-Path "build\index.html") {
    Write-Host "✅ Build completo! Iniciando servidor..." -ForegroundColor Green
    serve -s build -l 3000
} else {
    Write-Host "❌ Erro: index.html não foi criado" -ForegroundColor Red
    exit 1
}
