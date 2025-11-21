#!/usr/bin/env python3#!/usr/bin/env python3import sqlite3

"""

Script para corrigir e completar dados no banco de dados local"""

"""

Script para corrigir e completar dados no banco de dados local# Conectar ao banco

import os

import sys"""conn = sqlite3.connect('racket_hero.db')

from pathlib import Path

cursor = conn.cursor()

# Adicionar o diretório backend ao path

backend_path = Path(__file__).parentimport os

sys.path.insert(0, str(backend_path))

import sys# Verificar estrutura atual

from database import SessionLocal

from models import Usuario, Event, Player, EventoOrganizadorfrom pathlib import Pathprint("=== ESTRUTURA ATUAL DA TABELA player ===")



def fix_database():cursor.execute('PRAGMA table_info(player)')

    """Corrige problemas no banco de dados"""

    # Adicionar o diretório backend ao pathcolumns = cursor.fetchall()

    session = SessionLocal()

    backend_path = Path(__file__).parentfor col in columns:

    try:

        print("\n" + "="*70)sys.path.insert(0, str(backend_path))    print(f"  {col[1]}: {col[2]}")

        print("🔧 CORRIGINDO BANCO DE DADOS")

        print("="*70)

        

        # ===== PROBLEMA 1: Adicionar organizador ao evento =====from database import SessionLocal, engine, Base# Verificar se usuario_id já existe

        print("\n1️⃣  Adicionando organizador ao evento...")

        from models import Usuario, Event, Player, EventoOrganizadorhas_usuario_id = any(col[1] == 'usuario_id' for col in columns)

        event = session.query(Event).filter(Event.id == 1).first()

        organizador = session.query(Usuario).filter(Usuario.email == "organizador@test.com").first()

        

        if event and organizador:def fix_database():if not has_usuario_id:

            existing = session.query(EventoOrganizador).filter(

                EventoOrganizador.event_id == event.id,    """Corrige problemas no banco de dados"""    print("\n❌ Coluna usuario_id NÃO existe. Adicionando...")

                EventoOrganizador.usuario_id == organizador.id

            ).first()        try:

            

            if not existing:    session = SessionLocal()        cursor.execute('ALTER TABLE player ADD COLUMN usuario_id INTEGER')

                org_mapping = EventoOrganizador(

                    event_id=event.id,            conn.commit()

                    usuario_id=organizador.id,

                    é_criador=1    try:        print("✅ Coluna usuario_id adicionada com sucesso!")

                )

                session.add(org_mapping)        print("\n" + "="*70)    except Exception as e:

                session.commit()

                print(f"  ✅ Organizador '{organizador.nome}' adicionado ao evento '{event.name}'")        print("🔧 CORRIGINDO BANCO DE DADOS")        print(f"❌ Erro ao adicionar coluna: {e}")

            else:

                print(f"  ⏭️  Organizador já está mapeado para o evento")        print("="*70)else:

        else:

            print(f"  ❌ Evento ou organizador não encontrado")            print("\n✅ Coluna usuario_id JÁ existe!")

        

        # ===== PROBLEMA 2: Criar os 10 jogadores faltantes =====        # ===== PROBLEMA 1: Adicionar organizador ao evento =====

        print("\n2️⃣  Adicionando 10 jogadores de teste...")

                print("\n1️⃣  Adicionando organizador ao evento...")# Verificar novamente

        jogadores = [

            {"nome": "João Silva", "email": "joao.silva@example.com"},        print("\n=== ESTRUTURA APÓS ALTERAÇÃO ===")

            {"nome": "Maria Santos", "email": "maria.santos@example.com"},

            {"nome": "Pedro Oliveira", "email": "pedro.oliveira@example.com"},        # Verificar se o mapeamento já existecursor.execute('PRAGMA table_info(player)')

            {"nome": "Ana Costa", "email": "ana.costa@example.com"},

            {"nome": "Lucas Ferreira", "email": "lucas.ferreira@example.com"},        event = session.query(Event).filter(Event.id == 1).first()columns = cursor.fetchall()

            {"nome": "Patricia Alves", "email": "patricia.alves@example.com"},

            {"nome": "Roberto Gomes", "email": "roberto.gomes@example.com"},        organizador = session.query(Usuario).filter(Usuario.email == "organizador@test.com").first()for col in columns:

            {"nome": "Juliana Rocha", "email": "juliana.rocha@example.com"},

            {"nome": "Bruno Martins", "email": "bruno.martins@example.com"},            print(f"  {col[1]}: {col[2]}")

            {"nome": "Camila Ribeiro", "email": "camila.ribeiro@example.com"},

        ]        if event and organizador:

        

        for jog_data in jogadores:            existing = session.query(EventoOrganizador).filter(# Verificar dados do "Jogador Teste"

            existing_user = session.query(Usuario).filter(Usuario.email == jog_data["email"]).first()

            if not existing_user:                EventoOrganizador.event_id == event.id,print("\n=== PLAYERS DO JOGADOR TESTE ===")

                novo_usuario = Usuario(

                    nome=jog_data["nome"],                EventoOrganizador.usuario_id == organizador.idcursor.execute('SELECT id, event_id, name, usuario_id FROM player WHERE name LIKE "%Jogador%"')

                    email=jog_data["email"],

                    senha_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",            ).first()for row in cursor.fetchall():

                    tipo="jogador",

                    ativo=True                print(f"  ID: {row[0]}, EventID: {row[1]}, Nome: {row[2]}, UsuarioID: {row[3]}")

                )

                session.add(novo_usuario)            if not existing:

                session.commit()

                session.refresh(novo_usuario)                org_mapping = EventoOrganizador(# Se não estão vinculados, vincular agora

                print(f"  ✅ Usuário criado: {jog_data['nome']}")

            else:                    event_id=event.id,print("\n=== VINCULANDO JOGADOR TESTE AO USUÁRIO ===")

                novo_usuario = existing_user

                print(f"  ⏭️  Usuário já existe: {jog_data['nome']}")                    usuario_id=organizador.id,cursor.execute('SELECT id FROM usuarios WHERE email = ?', ('jogador@test.com',))

        

        # ===== PROBLEMA 3: Adicionar jogadores como Players ao evento =====                    é_criador=1user_result = cursor.fetchone()

        print("\n3️⃣  Vinculando jogadores ao evento (como Players)...")

                        )

        if event:

            for jog_data in jogadores:                session.add(org_mapping)if user_result:

                user = session.query(Usuario).filter(Usuario.email == jog_data["email"]).first()

                                session.commit()    user_id = user_result[0]

                if user:

                    existing_player = session.query(Player).filter(                print(f"  ✅ Organizador '{organizador.nome}' adicionado ao evento '{event.name}'")    print(f"Usuário ID encontrado: {user_id}")

                        Player.event_id == event.id,

                        Player.usuario_id == user.id            else:    

                    ).first()

                                    print(f"  ⏭️  Organizador já está mapeado para o evento")    cursor.execute(

                    if not existing_player:

                        player = Player(        else:        'UPDATE player SET usuario_id = ? WHERE name = ? AND usuario_id IS NULL',

                            event_id=event.id,

                            usuario_id=user.id,            print(f"  ❌ Evento ou organizador não encontrado")        (user_id, 'Jogador Teste')

                            name=user.nome,

                            initial_elo=1600.0            )

                        )

                        session.add(player)        # ===== PROBLEMA 2: Criar os 10 jogadores faltantes =====    affected = cursor.rowcount

                        print(f"  ✅ Jogador vinculado: {user.nome}")

                    else:        print("\n2️⃣  Adicionando 10 jogadores de teste...")    conn.commit()

                        print(f"  ⏭️  Jogador já está vinculado: {user.nome}")

                    print(f"✅ {affected} registros atualizados")

        session.commit()

                jogadores = [else:

        # ===== RESUMO FINAL =====

        print("\n" + "="*70)            {"nome": "João Silva", "email": "joao.silva@example.com"},    print("❌ Usuário jogador@test.com não encontrado")

        print("📊 STATUS FINAL")

        print("="*70)            {"nome": "Maria Santos", "email": "maria.santos@example.com"},

        

        usuarios_total = session.query(Usuario).count()            {"nome": "Pedro Oliveira", "email": "pedro.oliveira@example.com"},# Verificar após vinculação

        usuarios_org = session.query(Usuario).filter(Usuario.tipo == "organizador").count()

        usuarios_jog = session.query(Usuario).filter(Usuario.tipo == "jogador").count()            {"nome": "Ana Costa", "email": "ana.costa@example.com"},print("\n=== RESULTADO FINAL ===")

        eventos_total = session.query(Event).count()

        players_total = session.query(Player).count()            {"nome": "Lucas Ferreira", "email": "lucas.ferreira@example.com"},cursor.execute('SELECT id, event_id, name, usuario_id FROM player WHERE name LIKE "%Jogador%"')

        org_maping_total = session.query(EventoOrganizador).count()

                    {"nome": "Patricia Alves", "email": "patricia.alves@example.com"},for row in cursor.fetchall():

        print(f"\n  👥 Usuários: {usuarios_total}")

        print(f"     - Organizadores: {usuarios_org}")            {"nome": "Roberto Gomes", "email": "roberto.gomes@example.com"},    cursor.execute('SELECT name FROM event WHERE id = ?', (row[1],))

        print(f"     - Jogadores: {usuarios_jog}")

        print(f"  📅 Eventos: {eventos_total}")            {"nome": "Juliana Rocha", "email": "juliana.rocha@example.com"},    event_name = cursor.fetchone()

        print(f"  ⚽ Players (jogadores de eventos): {players_total}")

        print(f"  🔐 Mapeamentos Evento-Organizador: {org_maping_total}")            {"nome": "Bruno Martins", "email": "bruno.martins@example.com"},    print(f"  Player: {row[2]} (ID:{row[0]}), Evento: {event_name[0]} (ID:{row[1]}), UsuarioID: {row[3]}")

        

        print("\n✅ Banco de dados corrigido com sucesso!")            {"nome": "Camila Ribeiro", "email": "camila.ribeiro@example.com"},

        print("="*70 + "\n")

                ]conn.close()

        return True

                print("\n✅ Processo completo!")

    except Exception as e:

        print(f"\n❌ Erro ao corrigir banco de dados: {e}")        for jog_data in jogadores:

        import traceback            # Verificar se usuário já existe

        traceback.print_exc()            existing_user = session.query(Usuario).filter(Usuario.email == jog_data["email"]).first()

        session.rollback()            if not existing_user:

        return False                # Criar usuário

    finally:                novo_usuario = Usuario(

        session.close()                    nome=jog_data["nome"],

                    email=jog_data["email"],

if __name__ == "__main__":                    senha_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",  # Senha123!

    fix_database()                    tipo="jogador",

                    ativo=True
                )
                session.add(novo_usuario)
                session.commit()
                session.refresh(novo_usuario)
                print(f"  ✅ Usuário criado: {jog_data['nome']}")
            else:
                novo_usuario = existing_user
                print(f"  ⏭️  Usuário já existe: {jog_data['nome']}")
        
        session.commit()
        
        # ===== PROBLEMA 3: Adicionar os jogadores como Players ao evento =====
        print("\n3️⃣  Vinculando jogadores ao evento (como Players)...")
        
        if event:
            for jog_data in jogadores:
                user = session.query(Usuario).filter(Usuario.email == jog_data["email"]).first()
                
                if user:
                    # Verificar se já está como Player no evento
                    existing_player = session.query(Player).filter(
                        Player.event_id == event.id,
                        Player.usuario_id == user.id
                    ).first()
                    
                    if not existing_player:
                        player = Player(
                            event_id=event.id,
                            usuario_id=user.id,
                            name=user.nome,
                            initial_elo=1600.0
                        )
                        session.add(player)
                        print(f"  ✅ Jogador vinculado: {user.nome}")
                    else:
                        print(f"  ⏭️  Jogador já está vinculado: {user.nome}")
        
        session.commit()
        
        # ===== RESUMO FINAL =====
        print("\n" + "="*70)
        print("📊 STATUS FINAL")
        print("="*70)
        
        usuarios_total = session.query(Usuario).count()
        usuarios_org = session.query(Usuario).filter(Usuario.tipo == "organizador").count()
        usuarios_jog = session.query(Usuario).filter(Usuario.tipo == "jogador").count()
        eventos_total = session.query(Event).count()
        players_total = session.query(Player).count()
        org_maping_total = session.query(EventoOrganizador).count()
        
        print(f"\n  👥 Usuários: {usuarios_total}")
        print(f"     - Organizadores: {usuarios_org}")
        print(f"     - Jogadores: {usuarios_jog}")
        print(f"  📅 Eventos: {eventos_total}")
        print(f"  ⚽ Players (jogadores de eventos): {players_total}")
        print(f"  🔐 Mapeamentos Evento-Organizador: {org_maping_total}")
        
        print("\n✅ Banco de dados corrigido com sucesso!")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao corrigir banco de dados: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    fix_database()
