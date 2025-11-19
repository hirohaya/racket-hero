# test_integration.ps1 - Teste de integração completo

Write-Host "========================================" -ForegroundColor Green
Write-Host "TESTE DE INTEGRAÇÃO - RACKET HERO"  -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$baseUrl = "http://127.0.0.1:8000"

# 1. Health Check
Write-Host "`n[1] Testando Health Check..." -ForegroundColor Cyan
$response = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing
$health = $response.Content | ConvertFrom-Json
Write-Host "[OK] API respondendo - Status: $($health.status)" -ForegroundColor Green

# 2. Registrar novo usuário
Write-Host "`n[2] Registrando novo usuário..." -ForegroundColor Cyan
$registerBody = @{
    email = "teste_$(Get-Random)@test.com"
    nome = "Test User"
    password = "Senha123!@"
    tipo = "organizador"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $registerBody `
        -ErrorAction SilentlyContinue
    
    if ($response.StatusCode -eq 201) {
        $user = $response.Content | ConvertFrom-Json
        Write-Host "[OK] Usuário registrado! Token recebido" -ForegroundColor Green
        $token = $user.access_token
    } else {
        Write-Host "[ERROR] Status $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Testar logs criados
Write-Host "`n[3] Verificando logs criados..." -ForegroundColor Cyan
$logFile = "c:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend\logs\app.log"
if (Test-Path $logFile) {
    $logSize = (Get-Item $logFile).Length
    $logLines = (Get-Content $logFile | Measure-Object -Line).Lines
    Write-Host "[OK] Log criado: $logSize bytes, $logLines linhas" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Log não encontrado" -ForegroundColor Red
}

# 4. Testar backup
Write-Host "`n[4] Testando endpoint de admin..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/admin/system/health" `
        -UseBasicParsing `
        -ErrorAction SilentlyContinue
    
    if ($response.StatusCode -eq 200) {
        $health = $response.Content | ConvertFrom-Json
        Write-Host "[OK] Admin endpoint respondendo" -ForegroundColor Green
        Write-Host "    - Database size: $($health.database.size_mb) MB" -ForegroundColor Gray
        Write-Host "    - Total backups: $($health.backups.total)" -ForegroundColor Gray
    } else {
        Write-Host "[ERROR] Status $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Teste de validação
Write-Host "`n[5] Testando validação de entrada..." -ForegroundColor Cyan
$invalidBody = @{
    email = "email_invalido"
    nome = "Test"
    password = "fraca"
    tipo = "jogador"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $invalidBody `
        -ErrorAction SilentlyContinue `
        -WarningAction SilentlyContinue
    
    if ($response.StatusCode -eq 422) {
        Write-Host "[OK] Validação funcionando - Email inválido rejeitado (422)" -ForegroundColor Green
    }
} catch [Microsoft.PowerShell.Commands.HttpResponseException] {
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "[OK] Validação funcionando - Entrada inválida rejeitada (422)" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Status inesperado: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "TESTE CONCLUÍDO" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green
