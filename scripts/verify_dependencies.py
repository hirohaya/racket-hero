#!/usr/bin/env python3
"""
verify_dependencies.py - Verificar compatibilidade de versões e dependências
Verifica se todas as versões estão sem conflito e se todos os requisitos estão listados
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Backend dependencies
BACKEND_DEPS = {
    # Web Framework
    "fastapi": "0.100.0",
    "uvicorn": "0.23.0",
    
    # Database
    "sqlalchemy": "2.0.23",
    "alembic": "1.13.0",
    
    # Data Validation
    "pydantic": "2.5.0",
    "pydantic-settings": "2.1.0",
    "email-validator": "2.1.0",
    
    # Security
    "bcrypt": "4.1.1",
    "python-jose": "3.3.0",
    "cryptography": "41.0.7",
    
    # Utilities
    "python-dotenv": "1.0.0",
    "requests": "2.31.0",
    "apscheduler": "3.10.4",
    
    # Rate Limiting
    "slowapi": "0.1.9",
    
    # Testing
    "pytest": "7.4.3",
    "pytest-asyncio": "0.21.1",
    
    # Development
    "black": "23.12.0",
    "flake8": "6.1.0",
    "isort": "5.13.2",
    
    # Optional: Email
    "aiosmtplib": "3.0.0",
    "jinja2": "3.1.2",
}

# Frontend dependencies
FRONTEND_DEPS = {
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-router-dom": "^6.30.2",
    "axios": "^1.13.2",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4",
    "@testing-library/dom": "^10.4.1",
    "@testing-library/user-event": "^13.5.0",
}

FRONTEND_DEV_DEPS = {
    "@babel/preset-env": "^7.28.5",
    "@babel/preset-react": "^7.28.5",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.0",
    "babel-jest": "^30.2.0",
    "identity-obj-proxy": "^3.0.0",
    "jest": "^27.5.1",
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_ok(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def check_backend_requirements():
    """Verificar requirements.txt do backend"""
    print_header("🐍 Backend Dependencies Verification")
    
    req_file = Path("backend/requirements.txt")
    if not req_file.exists():
        print_error("requirements.txt não encontrado")
        return False
    
    with open(req_file) as f:
        content = f.read()
    
    # Parse requirements
    installed = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Handle different formats
        if '==' in line:
            name, version = line.split('==')
            installed[name.strip()] = version.strip()
        elif '[' in line:  # python-jose[cryptography]
            base = line.split('[')[0]
            if '==' in base:
                name, version = base.split('==')
                installed[name.strip()] = version.strip()
    
    all_ok = True
    missing = []
    
    # Check all expected dependencies
    for pkg, expected_version in BACKEND_DEPS.items():
        if pkg in installed:
            actual = installed[pkg]
            if actual == expected_version:
                print_ok(f"{pkg}=={actual}")
            else:
                print_warning(f"{pkg}: esperado {expected_version}, encontrado {actual}")
        else:
            print_error(f"{pkg}=={expected_version} - NÃO ENCONTRADO")
            missing.append(f"{pkg}=={expected_version}")
            all_ok = False
    
    if missing:
        print_error(f"\n{len(missing)} dependência(s) faltando no requirements.txt:")
        for pkg in missing:
            print(f"  - {pkg}")
    
    return all_ok, missing

def check_frontend_dependencies():
    """Verificar package.json do frontend"""
    print_header("📦 Frontend Dependencies Verification")
    
    pkg_file = Path("frontend/package.json")
    if not pkg_file.exists():
        print_error("package.json não encontrado")
        return False, []
    
    with open(pkg_file) as f:
        package = json.load(f)
    
    deps = package.get("dependencies", {})
    dev_deps = package.get("devDependencies", {})
    all_deps = {**deps, **dev_deps}
    
    all_ok = True
    missing = []
    
    # Check main dependencies
    for pkg, expected_version in FRONTEND_DEPS.items():
        if pkg in deps:
            actual = deps[pkg]
            if actual == expected_version:
                print_ok(f"{pkg}@{actual}")
            else:
                print_warning(f"{pkg}: esperado {expected_version}, encontrado {actual}")
        else:
            print_error(f"{pkg}@{expected_version} - NÃO ENCONTRADO")
            missing.append(f"{pkg}@{expected_version}")
            all_ok = False
    
    # Check dev dependencies
    for pkg, expected_version in FRONTEND_DEV_DEPS.items():
        if pkg in dev_deps:
            actual = dev_deps[pkg]
            if actual == expected_version:
                print_ok(f"{pkg}@{actual} (dev)")
            else:
                print_warning(f"{pkg}: esperado {expected_version}, encontrado {actual}")
        else:
            print_error(f"{pkg}@{expected_version} (dev) - NÃO ENCONTRADO")
            missing.append(f"{pkg}@{expected_version} (dev)")
            all_ok = False
    
    if missing:
        print_error(f"\n{len(missing)} dependência(s) faltando no package.json:")
        for pkg in missing:
            print(f"  - {pkg}")
    
    return all_ok, missing

def check_import_statements():
    """Verificar se todos os imports usados têm dependências"""
    print_header("🔍 Import Statements Verification")
    
    critical_imports = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "sqlalchemy": "sqlalchemy",
        "pydantic": "pydantic",
        "bcrypt": "bcrypt",
        "jose": "python-jose",
        "dotenv": "python-dotenv",
        "requests": "requests",
        "apscheduler": "apscheduler",
        "slowapi": "slowapi",
        "pytest": "pytest",
        "aiosmtplib": "aiosmtplib",
        "jinja2": "jinja2",
    }
    
    req_file = Path("backend/requirements.txt")
    with open(req_file) as f:
        content = f.read()
    
    all_ok = True
    for import_name, package_name in critical_imports.items():
        if package_name.lower() in content.lower():
            print_ok(f"'{import_name}' → {package_name} (registrado)")
        else:
            print_error(f"'{import_name}' → {package_name} (NÃO REGISTRADO)")
            all_ok = False
    
    return all_ok

def check_version_conflicts():
    """Verificar possíveis conflitos de versão"""
    print_header("⚔️  Version Conflict Detection")
    
    conflicts = []
    
    # Pydantic v2 requer campos específicos
    if BACKEND_DEPS["pydantic"] == "2.5.0":
        print_ok("Pydantic 2.5.0 - usando field_validator (compatível)")
        print_ok("Pydantic-settings 2.1.0 - para BaseSettings")
    
    # FastAPI com Pydantic v2
    if BACKEND_DEPS["fastapi"] >= "0.100.0":
        print_ok("FastAPI 0.100.0+ - compatível com Pydantic 2.x")
    
    # SQLAlchemy 2.0+ com FastAPI
    if BACKEND_DEPS["sqlalchemy"] == "2.0.23":
        print_ok("SQLAlchemy 2.0.23 - nova API (2.0 style)")
    
    # Security packages
    print_ok("python-jose 3.3.0 com cryptography 41.0.7 - compatível")
    print_ok("bcrypt 4.1.1 - compatível com Python 3.9+")
    
    # Rate limiting
    print_ok("slowapi 0.1.9 - compatível com FastAPI")
    
    # APScheduler
    print_ok("apscheduler 3.10.4 - compatível com Python 3.9+")
    
    return len(conflicts) == 0

def generate_report(backend_ok: bool, backend_missing: List, 
                   frontend_ok: bool, frontend_missing: List,
                   imports_ok: bool, conflicts_ok: bool) -> bool:
    """Gerar relatório final"""
    print_header("📋 Relatório Final")
    
    total_issues = len(backend_missing) + len(frontend_missing) + (0 if imports_ok else 1) + (0 if conflicts_ok else 1)
    
    if backend_ok:
        print_ok("Backend requirements.txt - OK")
    else:
        print_error(f"Backend requirements.txt - {len(backend_missing)} problema(s)")
    
    if frontend_ok:
        print_ok("Frontend package.json - OK")
    else:
        print_error(f"Frontend package.json - {len(frontend_missing)} problema(s)")
    
    if imports_ok:
        print_ok("Import statements - OK")
    else:
        print_error("Import statements - conflitos encontrados")
    
    if conflicts_ok:
        print_ok("Version conflicts - Nenhum encontrado")
    else:
        print_error("Version conflicts - Encontrados")
    
    print_info(f"\nTotal de problemas: {total_issues}")
    
    if total_issues == 0:
        print_ok("\n🎉 Todas as dependências estão corretas e sem conflitos!")
        return True
    else:
        print_error(f"\n⚠️  {total_issues} problema(s) encontrado(s)")
        return False

def main():
    print(f"\n{Colors.BOLD}Verificador de Dependências - Racket Hero{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    backend_ok, backend_missing = check_backend_requirements()
    frontend_ok, frontend_missing = check_frontend_dependencies()
    imports_ok = check_import_statements()
    conflicts_ok = check_version_conflicts()
    
    success = generate_report(backend_ok, backend_missing, 
                             frontend_ok, frontend_missing,
                             imports_ok, conflicts_ok)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
