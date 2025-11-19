#!/usr/bin/env python3
"""
fix_user_types.py - Corrige tipos de usuários do banco de dados

Converte tipos legados para os novos tipos do enum TipoUsuario:
- "usuario" → "jogador"
- "organizador" → mantém "organizador"
- "admin" → mantém "admin"
"""

import sys
from pathlib import Path

# Adiciona backend ao path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database import SessionLocal, init_db
from models.usuario import Usuario, TipoUsuario

def fix_user_types():
    """Corrige tipos de usuários no banco"""
    print("=" * 70)
    print("CORRIGINDO TIPOS DE USUÁRIOS")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # Usuários com tipo "usuario" → mudar para "jogador"
        usuarios_tipo_usuario = db.query(Usuario).filter(Usuario.tipo == "usuario").all()
        
        if usuarios_tipo_usuario:
            print(f"\n[INFO] Encontrados {len(usuarios_tipo_usuario)} usuários com tipo 'usuario'")
            print("Convertendo para 'jogador'...\n")
            
            for usuario in usuarios_tipo_usuario:
                print(f"  ✓ {usuario.email}: usuario → jogador")
                usuario.tipo = TipoUsuario.JOGADOR
        else:
            print("\n[INFO] Nenhum usuário com tipo 'usuario' encontrado")
        
        # Usuários com tipo "organizador" → converter para enum se necessário
        usuarios_tipo_org = db.query(Usuario).filter(Usuario.tipo == "organizador").all()
        
        if usuarios_tipo_org:
            print(f"\n[INFO] Encontrados {len(usuarios_tipo_org)} usuários com tipo 'organizador'")
            print("Garantindo que são o tipo enum correto...\n")
            
            for usuario in usuarios_tipo_org:
                if usuario.tipo != TipoUsuario.ORGANIZADOR.value:
                    print(f"  ✓ {usuario.email}: organizador → {TipoUsuario.ORGANIZADOR.value}")
                    usuario.tipo = TipoUsuario.ORGANIZADOR
                else:
                    print(f"  ⊘ {usuario.email}: já está correto")
        
        # Usuários com tipo "admin" → converter para enum se necessário
        usuarios_tipo_admin = db.query(Usuario).filter(Usuario.tipo == "admin").all()
        
        if usuarios_tipo_admin:
            print(f"\n[INFO] Encontrados {len(usuarios_tipo_admin)} usuários com tipo 'admin'")
            print("Garantindo que são o tipo enum correto...\n")
            
            for usuario in usuarios_tipo_admin:
                if usuario.tipo != TipoUsuario.ADMIN.value:
                    print(f"  ✓ {usuario.email}: admin → {TipoUsuario.ADMIN.value}")
                    usuario.tipo = TipoUsuario.ADMIN
                else:
                    print(f"  ⊘ {usuario.email}: já está correto")
        
        # Commit das mudanças
        db.commit()
        
        print("\n" + "=" * 70)
        print("[OK] TIPOS DE USUÁRIOS CORRIGIDOS COM SUCESSO!")
        print("=" * 70)
        
        # Exibe resumo final
        print("\n[INFO] Resumo final de usuários:")
        
        # Faz uma nova query para pegar dados atualizados
        usuarios = db.query(Usuario).all()
        tipos_count = {}
        
        for usuario in usuarios:
            tipo = usuario.tipo
            if tipo not in tipos_count:
                tipos_count[tipo] = []
            tipos_count[tipo].append(usuario.email)
        
        for tipo, emails in tipos_count.items():
            print(f"\n  {tipo} ({len(emails)}):")
            for email in emails:
                print(f"    • {email}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Erro ao corrigir tipos: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = fix_user_types()
    sys.exit(0 if success else 1)
