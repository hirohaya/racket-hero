#!/usr/bin/env bash

# Configuração de ambientes para Racket Hero
# Uso: ./scripts/setup-environment.sh [dev|staging|prod]

set -e

ENVIRONMENT=${1:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Racket Hero - Setup Environment${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Validar ambiente
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
    echo -e "${RED}❌ Invalid environment: $ENVIRONMENT${NC}"
    echo "Usage: ./scripts/setup-environment.sh [dev|staging|prod]"
    exit 1
fi

echo -e "${YELLOW}Environment: $ENVIRONMENT${NC}"
echo ""

# Função para carregar variáveis
load_env_vars() {
    local env=$1
    local env_file="$PROJECT_ROOT/.env.$env"
    
    if [ ! -f "$env_file" ]; then
        echo -e "${YELLOW}⚠️  Creating $env_file template...${NC}"
        case $env in
            dev)
                cat > "$env_file" << 'EOF'
ENVIRONMENT=development
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgresql://user:pass@localhost:5432/racket_hero_dev
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENVIRONMENT=development
BACKUP_ENABLED=false
EOF
                ;;
            staging)
                cat > "$env_file" << 'EOF'
ENVIRONMENT=staging
NODE_ENV=production
LOG_LEVEL=info
DATABASE_URL=postgresql://user:pass@railway.internal:5432/racket_hero_staging
CORS_ORIGINS=https://racket-hero-staging.railway.app
REACT_APP_API_URL=https://racket-hero-staging.railway.app/api
REACT_APP_ENVIRONMENT=staging
BACKUP_ENABLED=true
EOF
                ;;
            prod)
                cat > "$env_file" << 'EOF'
ENVIRONMENT=production
NODE_ENV=production
LOG_LEVEL=warn
DATABASE_URL=postgresql://user:pass@railway.internal:5432/racket_hero_prod
CORS_ORIGINS=https://racket-hero.app
REACT_APP_API_URL=https://racket-hero.app/api
REACT_APP_ENVIRONMENT=production
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
EOF
                ;;
        esac
        echo -e "${GREEN}✅ Created $env_file${NC}"
        echo -e "${YELLOW}⚠️  Update with real values!${NC}"
    fi
    
    # Load variables
    if [ -f "$env_file" ]; then
        set -a
        source "$env_file"
        set +a
    fi
}

# Função para verificar dependências
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    local missing=0
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js not found${NC}"
        missing=1
    else
        echo -e "${GREEN}✅ Node.js $(node -v)${NC}"
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm not found${NC}"
        missing=1
    else
        echo -e "${GREEN}✅ npm $(npm -v)${NC}"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        missing=1
    else
        echo -e "${GREEN}✅ Python $(python3 --version)${NC}"
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✅ Docker $(docker --version)${NC}"
    else
        echo -e "${YELLOW}⚠️  Docker not found (optional)${NC}"
    fi
    
    if [ $missing -eq 1 ]; then
        echo -e "${RED}❌ Missing dependencies!${NC}"
        exit 1
    fi
    
    echo ""
}

# Função para instalar dependências
install_dependencies() {
    echo -e "${BLUE}Installing dependencies...${NC}"
    
    # Backend
    if [ -d "$PROJECT_ROOT/backend" ]; then
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        cd "$PROJECT_ROOT/backend"
        
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate || . venv/Scripts/activate
        pip install -r requirements.txt
        deactivate
        
        echo -e "${GREEN}✅ Backend dependencies installed${NC}"
    fi
    
    # Frontend
    if [ -d "$PROJECT_ROOT/frontend" ]; then
        echo -e "${YELLOW}Installing Node dependencies...${NC}"
        cd "$PROJECT_ROOT/frontend"
        npm ci
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    fi
    
    echo ""
}

# Função para configurar banco de dados
setup_database() {
    echo -e "${BLUE}Setting up database...${NC}"
    
    case $ENVIRONMENT in
        dev)
            echo -e "${YELLOW}Creating development database...${NC}"
            cd "$PROJECT_ROOT/backend"
            python3 << 'PYTHON_EOF'
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

db_url = os.getenv('DATABASE_URL', 'sqlite:///./racket_hero_dev.db')
if not database_exists(db_url):
    create_database(db_url)
    print("✅ Development database created")
else:
    print("✅ Development database already exists")
PYTHON_EOF
            ;;
        staging|prod)
            echo -e "${YELLOW}Database must be created manually on Railway${NC}"
            echo -e "${YELLOW}Run migrations: cd backend && python -m alembic upgrade head${NC}"
            ;;
    esac
    
    echo ""
}

# Função para executar testes
run_tests() {
    echo -e "${BLUE}Running tests...${NC}"
    
    if [ "$ENVIRONMENT" = "dev" ]; then
        echo -e "${YELLOW}Running backend tests...${NC}"
        cd "$PROJECT_ROOT/backend"
        source venv/bin/activate || . venv/Scripts/activate
        pytest -v || true
        deactivate
        
        echo -e "${YELLOW}Running frontend tests...${NC}"
        cd "$PROJECT_ROOT/frontend"
        npm test -- --watchAll=false || true
    fi
    
    echo ""
}

# Função para iniciar servidor
start_servers() {
    echo -e "${BLUE}Starting servers...${NC}"
    
    if [ "$ENVIRONMENT" = "dev" ]; then
        echo -e "${YELLOW}Starting backend...${NC}"
        cd "$PROJECT_ROOT/backend"
        source venv/bin/activate || . venv/Scripts/activate
        python main.py &
        BACKEND_PID=$!
        
        echo -e "${YELLOW}Starting frontend...${NC}"
        cd "$PROJECT_ROOT/frontend"
        npm start &
        FRONTEND_PID=$!
        
        echo ""
        echo -e "${GREEN}✅ Servers started!${NC}"
        echo -e "${BLUE}Backend: http://localhost:8000${NC}"
        echo -e "${BLUE}Frontend: http://localhost:3000${NC}"
        echo ""
        echo "Press Ctrl+C to stop servers"
        
        wait
    else
        echo -e "${YELLOW}Skipping local server start for $ENVIRONMENT environment${NC}"
    fi
}

# Main execution
load_env_vars "$ENVIRONMENT"
check_dependencies
install_dependencies

if [ "$ENVIRONMENT" = "dev" ]; then
    setup_database
    run_tests
    start_servers
else
    echo -e "${BLUE}Environment: $ENVIRONMENT${NC}"
    echo -e "${GREEN}✅ Environment setup complete!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Configure secrets in GitHub Settings"
    echo "2. Create branches: git checkout -b develop && git checkout -b staging"
    echo "3. Push to repository: git push -u origin develop && git push -u origin staging"
    echo "4. Create Railway projects and link to branches"
fi

echo ""
