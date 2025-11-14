#!/usr/bin/env python3
"""
Script para criar contas de teste no backend.
Essas contas podem ser usadas para testar a aplicação sem precisar registrar.
"""

import os
import sys
import requests

# Adicionar backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal, init_db
from models.usuario import Usuario
from utils.security import hash_password

# Contas de teste a criar
TEST_ACCOUNTS = [
    {
        "name": "Admin Teste",
        "email": "admin@test.com",
        "password": "Senha123!",
        "role": "admin"
    },
    {
        "name": "Jogador Teste",
        "email": "jogador@test.com",
        "password": "Senha123!",
        "role": "player"
    },
    {
        "name": "Organizador Teste",
        "email": "organizador@test.com",
        "password": "Senha123!",
        "role": "organizer"
    }
]

def create_test_accounts_db():
    """Criar contas de teste diretamente no banco."""
    print("=" * 70)
    print("CRIANDO CONTAS DE TESTE")
    print("=" * 70)
    
    # Inicializar banco
    print("[*] Inicializando banco de dados...")
    init_db()
    print("[OK] Banco inicializado\n")
    
    db = SessionLocal()
    
    try:
        for account in TEST_ACCOUNTS:
            # Verificar se conta já existe
            existing = db.query(Usuario).filter(Usuario.email == account["email"]).first()
            if existing:
                print(f"[!] Conta {account['email']} já existe, pulando...")
                continue
            
            # Criar nova conta
            user = Usuario(
                nome=account["name"],
                email=account["email"],
                senha_hash=hash_password(account["password"]),
                ativo=True
            )
            db.add(user)
            db.flush()
            
            print(f"[OK] Conta criada:")
            print(f"    Email: {account['email']}")
            print(f"    Senha: {account['password']}")
            print(f"    Nome: {account['name']}\n")
        
        db.commit()
        
        print("=" * 70)
        print("[OK] CONTAS DE TESTE CRIADAS COM SUCESSO!")
        print("=" * 70)
        print("\nUse as seguintes credenciais para testar:\n")
        
        for account in TEST_ACCOUNTS:
            print(f"  {account['name']}")
            print(f"    📧 Email: {account['email']}")
            print(f"    🔑 Senha: {account['password']}\n")
        
    except Exception as e:
        print(f"\n[ERROR] Erro ao criar contas: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def create_test_accounts_api(api_url="http://localhost:8000"):
    """Criar contas de teste via API REST."""
    print("=" * 70)
    print("CRIANDO CONTAS DE TESTE VIA API")
    print("=" * 70)
    
    try:
        # Verificar se API está respondendo
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"[!] API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[!] Não foi possível conectar à API em {api_url}")
        return False
    
    print("[OK] API respondendo\n")
    
    for account in TEST_ACCOUNTS:
        try:
            # Tentar registrar conta
            response = requests.post(
                f"{api_url}/auth/register",
                json={
                    "nome": account["name"],
                    "email": account["email"],
                    "senha": account["password"]
                },
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                print(f"[OK] Conta criada: {account['email']}")
            elif response.status_code == 400:
                print(f"[!] Conta {account['email']} já existe")
            else:
                print(f"[!] Erro ao criar {account['email']}: {response.status_code}")
                
        except Exception as e:
            print(f"[!] Erro ao processar {account['email']}: {e}")
    
    print("\n" + "=" * 70)
    print("[OK] CONTAS DE TESTE PRONTAS!")
    print("=" * 70)

if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "db"
    
    if method == "api":
        create_test_accounts_api()
    else:
        create_test_accounts_db()
