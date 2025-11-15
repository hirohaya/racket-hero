#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import SessionLocal, init_db
from models.usuario import Usuario
from utils.security import verify_password

print("[1] Inicializando banco...")
init_db()

print("[2] Abrindo session...")
db = SessionLocal()

print("[3] Buscando usuário admin@test.com...")
usuario = db.query(Usuario).filter(Usuario.email == "admin@test.com").first()

if not usuario:
    print("   ❌ Usuário não encontrado!")
else:
    print(f"   ✅ Usuário encontrado: {usuario.nome}")
    print(f"   ID: {usuario.id}")
    print(f"   Email: {usuario.email}")
    print(f"   Ativo: {usuario.ativo}")
    
    print("[4] Verificando senha...")
    is_valid = verify_password("Senha123!", usuario.senha_hash)
    print(f"   Senha válida: {is_valid}")

db.close()
print("\n[OK] Teste completado")
