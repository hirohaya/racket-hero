#!/usr/bin/env python3
"""
railway_db_access.py - Helper para acessar banco de dados em produção no Railway

Uso:
    python railway_db_access.py --help
    python railway_db_access.py list-usuarios
    python railway_db_access.py query "SELECT * FROM event"
    python railway_db_access.py backup
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

class RailwayDBAccess:
    def __init__(self, ssh_host=None):
        """Inicializar acesso ao banco Railway"""
        self.ssh_host = ssh_host or self._get_ssh_host_from_env()
        self.db_path = "/app/racket_hero.db"
    
    def _get_ssh_host_from_env(self):
        """Obter SSH host das variáveis de ambiente"""
        import os
        host = os.getenv("RAILWAY_SSH_HOST")
        if not host:
            print("❌ RAILWAY_SSH_HOST não configurado")
            print("   Defina com: export RAILWAY_SSH_HOST='user@host'")
            sys.exit(1)
        return host
    
    def _execute_remote(self, command):
        """Executar comando remoto via SSH"""
        full_cmd = f'ssh {self.ssh_host} "{command}"'
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    
    def query(self, sql, output_format="table"):
        """Executar query no banco remoto"""
        sql_escaped = sql.replace('"', '\\"').replace('\n', ' ')
        
        if output_format == "json":
            cmd = f'cd /app && sqlite3 -json racket_hero.db "{sql_escaped}"'
        else:
            cmd = f'cd /app && sqlite3 racket_hero.db "{sql_escaped}"'
        
        stdout, stderr, code = self._execute_remote(cmd)
        
        if code != 0:
            print(f"❌ Erro ao executar query: {stderr}")
            return None
        
        if output_format == "json":
            try:
                return json.loads(stdout)
            except:
                return stdout
        return stdout
    
    def list_usuarios(self):
        """Listar todos os usuários"""
        print("\n📋 Usuários Cadastrados\n")
        sql = "SELECT id, nome, email, tipo FROM usuario LIMIT 20;"
        result = self.query(sql)
        print(result)
    
    def list_events(self):
        """Listar eventos"""
        print("\n📅 Eventos\n")
        sql = "SELECT id, nome, data, hora, ativo FROM event ORDER BY data DESC LIMIT 20;"
        result = self.query(sql)
        print(result)
    
    def list_players(self, event_id=None):
        """Listar jogadores"""
        if event_id:
            sql = f"SELECT id, nome, clube, elo_atual FROM player WHERE event_id = {event_id};"
        else:
            sql = "SELECT id, nome, clube, elo_atual FROM player ORDER BY elo_atual DESC LIMIT 20;"
        
        print(f"\n👥 Jogadores{f' - Evento {event_id}' if event_id else ''}\n")
        result = self.query(sql)
        print(result)
    
    def ranking(self, event_id=None):
        """Mostrar ranking ELO"""
        if event_id:
            sql = f"""
            SELECT 
                ROW_NUMBER() OVER (ORDER BY elo_atual DESC) as ranking,
                nome,
                elo_atual
            FROM player
            WHERE event_id = {event_id}
            ORDER BY elo_atual DESC;
            """
        else:
            sql = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY elo_atual DESC) as ranking,
                nome,
                elo_atual
            FROM player
            ORDER BY elo_atual DESC
            LIMIT 20;
            """
        
        print(f"\n🏆 Ranking ELO{f' - Evento {event_id}' if event_id else ''}\n")
        result = self.query(sql)
        print(result)
    
    def backup_database(self):
        """Fazer backup do banco"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"racket_hero_backup_{timestamp}.sql"
        
        cmd = f'cd /app && sqlite3 racket_hero.db .dump > {backup_file} && cat {backup_file}'
        stdout, stderr, code = self._execute_remote(cmd)
        
        if code != 0:
            print(f"❌ Erro ao fazer backup: {stderr}")
            return False
        
        # Salvar localmente
        with open(backup_file, "w") as f:
            f.write(stdout)
        
        print(f"✅ Backup salvo em: {backup_file}")
        print(f"   Tamanho: {len(stdout) / 1024:.2f} KB")
        return True
    
    def show_stats(self):
        """Mostrar estatísticas do banco"""
        print("\n📊 Estatísticas do Banco\n")
        
        queries = {
            "Total Usuários": "SELECT COUNT(*) as total FROM usuario;",
            "Total Eventos": "SELECT COUNT(*) as total FROM event;",
            "Total Jogadores": "SELECT COUNT(*) as total FROM player;",
            "Total Partidas": "SELECT COUNT(*) as total FROM match;",
            "Evento Mais Recente": "SELECT nome, data FROM event ORDER BY data DESC LIMIT 1;",
            "Jogador Top Ranking": "SELECT nome, elo_atual FROM player ORDER BY elo_atual DESC LIMIT 1;",
        }
        
        for label, sql in queries.items():
            result = self.query(sql).strip()
            print(f"{label}: {result}")
    
    def connect_ssh(self):
        """Conectar via SSH interativo"""
        import os
        cmd = f'ssh {self.ssh_host}'
        os.system(cmd)
    
    def sqlite_shell(self):
        """Abrir shell SQLite interativo"""
        cmd = f'ssh {self.ssh_host} "cd /app && sqlite3 racket_hero.db"'
        import os
        os.system(cmd)

def main():
    parser = argparse.ArgumentParser(
        description="Acesso ao banco de dados do Racket Hero em produção (Railway)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python railway_db_access.py stats              # Mostrar estatísticas
  python railway_db_access.py list-usuarios      # Listar usuários
  python railway_db_access.py list-events        # Listar eventos
  python railway_db_access.py ranking            # Mostrar ranking ELO
  python railway_db_access.py backup             # Fazer backup
  python railway_db_access.py query "SELECT *..."  # Executar query customizada
  python railway_db_access.py shell              # Abrir SQLite shell interativo
        """
    )
    
    parser.add_argument(
        "command",
        choices=[
            "stats", "list-usuarios", "list-events", "list-players",
            "ranking", "backup", "query", "shell", "ssh"
        ],
        help="Comando a executar"
    )
    
    parser.add_argument(
        "--ssh-host",
        help="SSH host (padrão: variável RAILWAY_SSH_HOST)"
    )
    
    parser.add_argument(
        "--event-id",
        type=int,
        help="ID do evento (para list-players e ranking)"
    )
    
    parser.add_argument(
        "query_text",
        nargs="?",
        help="Query SQL (para comando 'query')"
    )
    
    args = parser.parse_args()
    
    # Inicializar acesso
    try:
        db = RailwayDBAccess(args.ssh_host)
    except SystemExit:
        return 1
    
    # Executar comando
    if args.command == "stats":
        db.show_stats()
    elif args.command == "list-usuarios":
        db.list_usuarios()
    elif args.command == "list-events":
        db.list_events()
    elif args.command == "list-players":
        db.list_players(args.event_id)
    elif args.command == "ranking":
        db.ranking(args.event_id)
    elif args.command == "backup":
        db.backup_database()
    elif args.command == "query":
        if not args.query_text:
            print("❌ Query text obrigatório para comando 'query'")
            return 1
        result = db.query(args.query_text)
        print(result)
    elif args.command == "shell":
        print("🔌 Abrindo SQLite shell interativo...")
        print("   (use '.exit' para sair)\n")
        db.sqlite_shell()
    elif args.command == "ssh":
        print("🔌 Conectando via SSH...")
        db.connect_ssh()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
