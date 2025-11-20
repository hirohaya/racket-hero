#!/bin/bash
# start.sh - Script de inicialização para Railway
# Executa seed e depois inicia a aplicação

echo "🚀 Iniciando Racket Hero..."

# Executar seed de dados
echo "🌱 Executando seed de dados..."
python backend/seed_dev.py

# Iniciar o backend
echo "📡 Iniciando backend..."
cd backend
python main.py
