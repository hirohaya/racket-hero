#!/usr/bin/env python3
"""
Script para adicionar dados de teste ao banco de dados de dev
Adiciona 10 jogadores e 2 organizadores
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from database import SessionLocal, engine, Base
from models import Usuario
from datetime import datetime

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

session = SessionLocal()

try:
    # ============ ADICIONAR ORGANIZADORES ============
    print("\n📋 Adicionando Organizadores...")
    
    organizadores = [
        {
            "nome": "Carlos Souza",
            "email": "carlos@example.com",
            "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",  # password
            "tipo": "organizador",
            "ativo": True
        },
        {
            "nome": "Fernanda Lima",
            "email": "fernanda@example.com",
            "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",  # password
            "tipo": "organizador",
            "ativo": True
        }
    ]
    
    for org_data in organizadores:
        # Verificar se já existe
        existing = session.query(Usuario).filter(Usuario.email == org_data["email"]).first()
        if not existing:
            org = Usuario(**org_data)
            session.add(org)
            print(f"  ✅ Organizador adicionado: {org_data['nome']} ({org_data['email']})")
        else:
            print(f"  ⚠️  Organizador já existe: {org_data['nome']}")
    
    session.commit()
    
    # ============ ADICIONAR JOGADORES ============
    print("\n🎯 Adicionando Jogadores...")
    
    jogadores = [
        {"nome": "João Silva", "email": "joao.silva@example.com"},
        {"nome": "Maria Santos", "email": "maria.santos@example.com"},
        {"nome": "Pedro Oliveira", "email": "pedro.oliveira@example.com"},
        {"nome": "Ana Costa", "email": "ana.costa@example.com"},
        {"nome": "Lucas Ferreira", "email": "lucas.ferreira@example.com"},
        {"nome": "Patricia Alves", "email": "patricia.alves@example.com"},
        {"nome": "Roberto Gomes", "email": "roberto.gomes@example.com"},
        {"nome": "Juliana Rocha", "email": "juliana.rocha@example.com"},
        {"nome": "Bruno Martins", "email": "bruno.martins@example.com"},
        {"nome": "Camila Ribeiro", "email": "camila.ribeiro@example.com"},
    ]
    
    for jog_data in jogadores:
        # Verificar se já existe
        existing = session.query(Usuario).filter(Usuario.email == jog_data["email"]).first()
        if not existing:
            jog = Usuario(
                nome=jog_data["nome"],
                email=jog_data["email"],
                senha_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",  # password
                tipo="jogador",
                ativo=True
            )
            session.add(jog)
            print(f"  ✅ Jogador adicionado: {jog_data['nome']} ({jog_data['email']})")
        else:
            print(f"  ⚠️  Jogador já existe: {jog_data['nome']}")
    
    session.commit()
    
    # Contar total de usuários
    total_users = session.query(Usuario).count()
    total_orgs = session.query(Usuario).filter(Usuario.tipo == "organizador").count()
    total_players = session.query(Usuario).filter(Usuario.tipo == "jogador").count()
    
    print(f"\n📊 Resumo Final:")
    print(f"  Total de usuários: {total_users}")
    print(f"  Organizadores: {total_orgs}")
    print(f"  Jogadores: {total_players}")
    print(f"\n✅ Dados adicionados com sucesso!")
    print(f"\n💡 Credenciais para teste:")
    print(f"  Email: carlos@example.com")
    print(f"  Senha: password")
    print(f"  Tipo: Organizador")
    
except Exception as e:
    print(f"\n❌ Erro: {str(e)}")
    session.rollback()
    raise
finally:
    session.close()
