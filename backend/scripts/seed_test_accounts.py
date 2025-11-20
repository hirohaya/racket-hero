#!/usr/bin/env python3
"""
Script para criar contas de teste no banco de dados.
Cria contas de Jogador e Organizador para testing.

Uso:
    cd backend
    python scripts/seed_test_accounts.py
"""

import sys
import os
from pathlib import Path

# Adicionar diretório do backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal, engine, Base
from models.usuario import Usuario, TipoUsuario
from utils.security import hash_password

def seed_test_accounts():
    """Criar contas de teste no banco de dados"""
    
    print("\n" + "="*60)
    print("🌱 Seeding Contas de Teste")
    print("="*60)
    
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Dados das contas de teste
        test_accounts = [
            {
                "email": "jogador@test.com",
                "nome": "Jogador Teste",
                "senha": "Senha123!",
                "tipo": TipoUsuario.JOGADOR
            },
            {
                "email": "organizador@test.com",
                "nome": "Organizador Teste",
                "senha": "Senha123!",
                "tipo": TipoUsuario.ORGANIZADOR
            }
        ]
        
        # Criar cada conta
        for account in test_accounts:
            # Verificar se já existe
            usuario_existente = db.query(Usuario).filter(
                Usuario.email == account["email"]
            ).first()
            
            if usuario_existente:
                print(f"⏭️  Conta já existe: {account['email']} (id: {usuario_existente.id})")
                continue
            
            # Criar nova conta
            novo_usuario = Usuario(
                email=account["email"],
                nome=account["nome"],
                senha_hash=hash_password(account["senha"]),
                tipo=account["tipo"],
                ativo=True
            )
            
            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)
            
            print(f"✅ Conta criada: {novo_usuario.email} (tipo: {novo_usuario.tipo}, id: {novo_usuario.id})")
            print(f"   📧 Email: {novo_usuario.email}")
            print(f"   🔑 Senha: {account['senha']}")
            print(f"   👤 Tipo: {novo_usuario.tipo}")
            print()
        
        # Listar todas as contas
        print("="*60)
        print("📋 Contas Registradas no Sistema:")
        print("="*60)
        
        usuarios = db.query(Usuario).all()
        if usuarios:
            for usuario in usuarios:
                print(f"  • {usuario.email} ({usuario.tipo}) - {usuario.nome}")
        else:
            print("  Nenhuma conta encontrada")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Erro ao criar contas: {e}")
        db.rollback()
        sys.exit(1)
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_accounts()
