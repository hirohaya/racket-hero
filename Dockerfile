# Multi-stage build para Racket Hero

# Stage 1: Build do Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copiar package.json e package-lock.json
COPY frontend/package*.json ./

# Instalar dependências
RUN npm ci --omit=dev

# Copiar código do frontend
COPY frontend/src ./src
COPY frontend/public ./public

# Arquivo package.json para referência
COPY frontend/package.json .

# Build do React com API URL padrão (/api para modo relativo)
ENV REACT_APP_API_URL=/api
RUN npm run build

# Stage 2: Backend + Frontend servido
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (incluindo PostgreSQL client)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Copiar build do frontend do stage anterior
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Criar diretório de logs
RUN mkdir -p /app/logs

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=postgresql://user:password@localhost/racket_hero \
    CORS_ORIGINS=http://localhost:3000,http://localhost:8000 \
    LOG_LEVEL=info

# Iniciar aplicação
WORKDIR /app/backend
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
