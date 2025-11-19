#!/usr/bin/env python3
# scripts/validate_railway_setup.py
# Valida se o projeto está pronto para Railway

import os
import sys
import subprocess
from pathlib import Path
import json

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_status(msg: str, status: str = "INFO"):
    colors = {
        "OK": Colors.GREEN,
        "ERROR": Colors.RED,
        "WARNING": Colors.YELLOW,
        "INFO": Colors.BLUE
    }
    color = colors.get(status, Colors.BLUE)
    print(f"{color}[{status}]{Colors.RESET} {msg}")

def check_file_exists(path: str, description: str) -> bool:
    if Path(path).exists():
        print_status(f"✅ {description} encontrado", "OK")
        return True
    else:
        print_status(f"❌ {description} NÃO encontrado: {path}", "ERROR")
        return False

def check_python_packages() -> bool:
    """Verifica se todos os pacotes Python estão instalados"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print_status("✅ Todas as dependências Python instaladas", "OK")
        return True
    except ImportError as e:
        print_status(f"❌ Dependência Python faltando: {e}", "ERROR")
        return False

def check_node_packages() -> bool:
    """Verifica se node_modules está instalado"""
    if Path("frontend/node_modules").exists():
        print_status("✅ Dependências Node instaladas", "OK")
        return True
    else:
        print_status("⚠️  Node modules não encontrados - será instalado no Railway", "WARNING")
        return True  # Railway instala automaticamente

def check_database():
    """Verifica se banco de dados pode ser inicializado"""
    try:
        sys.path.insert(0, "backend")
        from database import init_db, engine
        
        init_db()
        print_status("✅ Banco de dados inicializado com sucesso", "OK")
        return True
    except Exception as e:
        print_status(f"❌ Erro ao inicializar banco: {e}", "ERROR")
        return False

def check_backend_imports():
    """Verifica se main.py pode ser importado"""
    try:
        sys.path.insert(0, "backend")
        import main
        print_status("✅ Backend main.py importa corretamente", "OK")
        return True
    except Exception as e:
        print_status(f"❌ Erro ao importar main.py: {e}", "ERROR")
        return False

def check_config_files() -> bool:
    """Verifica se arquivos de configuração Railway existem"""
    results = []
    results.append(check_file_exists("railway.toml", "railway.toml"))
    results.append(check_file_exists("Procfile", "Procfile"))
    results.append(check_file_exists(".env.railway", ".env.railway"))
    
    return all(results)

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚀 Validando Setup para Railway{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    checks = []
    
    # Check 1: Arquivos de configuração
    print(f"\n{Colors.BLUE}1️⃣ Verificando arquivos de configuração...{Colors.RESET}")
    checks.append(check_config_files())
    
    # Check 2: Backend
    print(f"\n{Colors.BLUE}2️⃣ Verificando Backend...{Colors.RESET}")
    checks.append(check_file_exists("backend/main.py", "backend/main.py"))
    checks.append(check_file_exists("backend/requirements.txt", "backend/requirements.txt"))
    checks.append(check_file_exists("backend/database.py", "backend/database.py"))
    checks.append(check_python_packages())
    checks.append(check_backend_imports())
    checks.append(check_database())
    
    # Check 3: Frontend
    print(f"\n{Colors.BLUE}3️⃣ Verificando Frontend...{Colors.RESET}")
    checks.append(check_file_exists("frontend/package.json", "frontend/package.json"))
    checks.append(check_file_exists("frontend/src", "frontend/src"))
    checks.append(check_node_packages())
    
    # Check 4: Git
    print(f"\n{Colors.BLUE}4️⃣ Verificando Git...{Colors.RESET}")
    checks.append(check_file_exists(".git", "Repositório Git"))
    
    # Resumo
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    passed = sum(checks)
    total = len(checks)
    
    if all(checks):
        print_status(f"✅ TODAS as verificações passaram! ({passed}/{total})", "OK")
        print(f"\n{Colors.GREEN}Seu projeto está pronto para Railway!{Colors.RESET}")
        print(f"\n{Colors.BLUE}Próximos passos:{Colors.RESET}")
        print(f"1. git add .")
        print(f"2. git commit -m 'Feat: Railway configuration'")
        print(f"3. git push origin main")
        print(f"4. Criar conta em https://railway.app")
        print(f"5. Conectar seu repositório GitHub")
        print(f"6. Railway faz deploy automaticamente! 🎉\n")
        return 0
    else:
        print_status(f"❌ Algumas verificações falharam ({passed}/{total})", "ERROR")
        print(f"\n{Colors.YELLOW}Corrija os erros acima antes de fazer deploy.{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
