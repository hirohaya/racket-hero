#!/usr/bin/env python3
"""
Script para criar mais contas de teste (9 jogadores + 1 organizador).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal, init_db
from models.usuario import Usuario
from utils.security import hash_password

# Contas adicionais para teste
ADDITIONAL_ACCOUNTS = [
    # 9 Jogadores
    {"name": "João Silva", "email": "joao@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Maria Santos", "email": "maria@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Pedro Oliveira", "email": "pedro@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Ana Costa", "email": "ana@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Carlos Mendes", "email": "carlos@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Patricia Lima", "email": "patricia@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Roberto Alves", "email": "roberto@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Fernanda Souza", "email": "fernanda@test.com", "password": "Senha123!", "role": "usuario"},
    {"name": "Lucas Martins", "email": "lucas@test.com", "password": "Senha123!", "role": "usuario"},
    
    # 1 Organizador adicional
    {"name": "Organizador 2", "email": "org2@test.com", "password": "Senha123!", "role": "organizador"},
]

def main():
    print("[1] Inicializando banco...")
    init_db()
    
    print("[2] Abrindo session...")
    db = SessionLocal()
    
    created = 0
    skipped = 0
    
    print("[3] Criando contas...")
    for account in ADDITIONAL_ACCOUNTS:
        # Verificar se email já existe
        existing = db.query(Usuario).filter(Usuario.email == account["email"]).first()
        
        if existing:
            print(f"   [SKIP] Pulando {account['email']} (ja existe)")
            skipped += 1
            continue
        
        # Criar novo usuário
        usuario = Usuario(
            email=account["email"],
            nome=account["name"],
            senha_hash=hash_password(account["password"]),
            tipo=account["role"],
            ativo=True
        )
        
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        print(f"   [OK] Criado: {account['email']} ({account['name']}) - {account['role']}")
        created += 1
    
    print(f"\n[RESULTADO]")
    print(f"   [OK] Criadas: {created} contas")
    print(f"   [SKIP] Puladas: {skipped} contas (ja existiam)")
    print(f"   [INFO] Total: {created + skipped} contas processadas")
    
    # Listar todas as contas
    print(f"\n[CONTAS DISPONIVEIS]")
    usuarios = db.query(Usuario).all()
    print(f"   Total de usuarios no banco: {len(usuarios)}")
    print()
    
    # Separar por tipo
    admins = [u for u in usuarios if u.tipo == "admin"]
    organizadores = [u for u in usuarios if u.tipo == "organizador"]
    jogadores = [u for u in usuarios if u.tipo == "usuario"]
    
    if admins:
        print("   [ADMIN]")
        for u in admins:
            print(f"      * {u.email} ({u.nome})")
    
    if organizadores:
        print("   [ORGANIZADOR]")
        for u in organizadores:
            print(f"      * {u.email} ({u.nome})")
    
    if jogadores:
        print("   [JOGADOR]")
        for u in jogadores:
            print(f"      * {u.email} ({u.nome})")
    
    db.close()
    print("\n[OK] Script concluído!")

if __name__ == "__main__":
    main()
