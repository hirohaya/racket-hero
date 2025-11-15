# 🧪 Quick Test Reference

## 🚀 Start Everything

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend  
cd frontend && npm start

# Terminal 3: View logs (optional)
tail -f logs/*.log
```

Then visit: **http://localhost:3000**

---

## 📋 Test Accounts

### 🔐 Administrator
```
Email: admin@test.com
Password: Senha123!
Type: ADMIN
Permissions: Everything
```

### 📋 Organizer (João)
```
Email: joao@eventos.com
Password: Senha123!
Type: ORGANIZADOR
Permissions: Create/Edit events, view all, see reports
```

### 📋 Organizer (Maria)
```
Email: maria@eventos.com
Password: Senha123!
Type: ORGANIZADOR
Permissions: Create/Edit events, view all, see reports
```

### 🎯 Player
```
Email: jogador@test.com
Password: Senha123!
Type: JOGADOR
Permissions: View events, view matches, view rankings
```

---

## 📊 Test Data Available

### Events (5 total)
1. **Campeonato Regional 2025** - 20/11/2025 @ 19:00
2. **Torneio Local - Novembro** - 18/11/2025 @ 18:30
3. **Casual Friday Night** - 16/11/2025 @ 20:00
4. **Campeonato Nacional - Fase Estadual** - 25/11/2025 @ 17:00
5. **Treino Semanal** - 15/11/2025 @ 18:00

### Players (15 total - 3 per event)
All players have initial ELO ratings between 1650-1950

### Quick Navigation
- **Home**: http://localhost:3000/
- **Events**: http://localhost:3000/eventos
- **Login**: http://localhost:3000/login

---

## 🧹 Reset Test Data

If you need fresh data:

```bash
cd tests
python create_test_data.py
```

This will:
- Clear old events & players
- Create 5 new events
- Create 15 new players
- Create 2 organizer accounts
- Sync database to backend

---

## 🔄 Recreate Test Data

If you deleted the database:

```bash
# Recreate user accounts
cd tests && python create_test_accounts.py

# Create events & players
python create_test_data.py

# Copy database to backend
cp racket_hero.db ../backend/racket_hero.db
```

---

## 🧪 Test Scenarios

### Scenario 1: Login as Organizer
1. Go to http://localhost:3000/login
2. Click "📋 Organizador joao@eventos.com Senha123!" button
3. Should see "João Silva" in header and "Bem-vindo ao Racket Hero" message
4. Click "Ver Eventos" to see all 5 events

### Scenario 2: View Event Details
1. From Events page, click "Editar" button on any event
2. Should load event details (name, date, time)
3. Click "Cancelar" to go back

### Scenario 3: Check Permissions
1. Login as JOGADOR (jogador@test.com)
2. Should see events but NOT "Novo Evento" button
3. Should be able to view but not edit

### Scenario 4: Admin Access
1. Login as ADMIN (admin@test.com)
2. Should see all features
3. Should be able to create, edit, delete events
4. Should be able to delete organizations

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database empty | Run `python tests/create_test_data.py` |
| Can't login | Check database is in `backend/` directory |
| No events showing | Refresh browser (Ctrl+R) |
| Token expired | Login again |
| Port 8000 in use | Kill backend: `pkill -f "python main.py"` |

---

## 📈 Performance Notes

- **5 events**: ~50ms to load
- **15 players**: ~20ms per event
- **Login**: ~100ms (with JWT verification)
- **Database**: ~2MB SQLite file

---

## 🔗 API Endpoints (with token required)

```bash
# Get all events (requires VER_EVENTOS permission)
GET /events

# Get event by ID
GET /events/{id}

# Create event (requires ORGANIZADOR)
POST /events

# Get players for event
GET /events/{id}/players

# Get ranking for event
GET /events/{id}/ranking
```

---

**Last Updated**: 15/11/2025
**Version**: 1.0
**Status**: ✅ Ready for testing
