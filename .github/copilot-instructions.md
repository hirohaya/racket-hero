# Racket Hero - AI Coding Agent Instructions

This document provides essential context for AI coding agents (GitHub Copilot, Claude, etc.) working on the Racket Hero project. Use this to understand architecture, conventions, and workflows.

## Project Overview

**Racket Hero** is a tournament management system for ping-pong events.

- **Status**: Low complexity, MVP phase
- **Tech Stack**: FastAPI + React + SQLite + SQLAlchemy
- **Database**: SQLite with 3 core entities (Groups, Events, Players, Matches)

## Coding Philosophy

- **Simplicity**: Prioritize clear, maintainable code over complex optimizations
- **Conventions**: Follow established patterns in existing code (see below)
- **Documentation**: Comment non-obvious logic; refer to this file for architecture/context
- **Virtual Environments**: Always works on and use virtual environments for Python dependencies; isolate frontend with npm
- **README Updates**: Keep `README.md` updated with architecture changes and project progress from tasks
- **Testing**: Always run a complete tests, unit and e2e after making any changes. 
- **Branch Cleaning**: Delete feature branches after merging to main to keep repo tidy
- **Terminal**: always close terminal sessions after use to avoid resource leaks

## Implementation & Testing Workflow

### 2. Development Cycle
1. **Make code changes** (backend, frontend, or both)
2. **Save files**
3. **Immediately test in browser** using Playwright MCP without generating code
4. **Verify changes** before moving to next feature
5. **Repeat** for each component/feature

### 3. Playwright MCP Testing Protocol

**Purpose**: Automated browser testing with real UI interaction

**When to Test**:
- ✅ After every backend endpoint modification
- ✅ After every frontend component change
- ✅ After database schema changes
- ✅ After service layer updates
- ✅ Before committing code to git

**Testing Approach**:
1. Navigate to relevant page: `mcp_microsoft_pla_browser_navigate(url)`
2. Wait for content to load: `mcp_microsoft_pla_browser_wait_for(time)`
3. Take snapshot of page state: `mcp_microsoft_pla_browser_snapshot()`
4. Interact with UI: click, type, select, fill forms
5. Verify results: check alerts, inspect page state, API responses
6. Test edge cases: validation, error states, empty states

**Example Test Flow**:
```
Navigate → Wait → Snapshot (verify page loaded)
→ Click button → Type text → Submit form
→ Check alert message → Verify data in list
→ Refresh page → Verify persistence
```

**Key Playwright Commands**:
- `mcp_microsoft_pla_browser_navigate(url)` - Navigate to page
- `mcp_microsoft_pla_browser_snapshot()` - Get page accessibility snapshot
- `mcp_microsoft_pla_browser_click(element, ref)` - Click element
- `mcp_microsoft_pla_browser_type(element, ref, text)` - Type into field
- `mcp_microsoft_pla_browser_select_option(element, ref, values)` - Select dropdown
- `mcp_microsoft_pla_browser_fill_form(fields)` - Fill multiple fields
- `mcp_microsoft_pla_browser_wait_for(time)` - Wait for time or condition
- `mcp_microsoft_pla_browser_handle_dialog(accept)` - Handle alert/confirm dialogs
- `mcp_microsoft_pla_browser_take_screenshot(filename)` - Take visual screenshot

### 4. Test Coverage Requirements

**Minimum Testing Per Feature**:
- ✅ Happy path (successful operation)
- ✅ Validation failures (invalid input)
- ✅ API error handling (404, 500, etc.)
- ✅ Data persistence (page refresh)
- ✅ Related features (rankings, calculations, etc.)

**For Match Creation** (example):
- Create match with valid data → verify appears in list
- Create match with invalid data → verify error message
- Create match without required field → verify validation alert
- Refresh page → verify match still exists
- Check rankings updated → verify Elo calculations

### 5. Success Criteria
- All Playwright tests pass without errors
- No browser console errors ([ERROR] messages)
- Form validation works as designed
- Data persists after page refresh
- Related calculations/rankings update correctly
- No breaking changes to existing features

### 6. Documentation of Test Results
After testing, only show results on chat, do not generate report files.

### 7. Common Testing Mistakes to Avoid
- ❌ Making changes without running backend/frontend
- ❌ Skipping browser testing and only running unit tests
- ❌ Not waiting for async operations (use `mcp_microsoft_pla_browser_wait_for`)
- ❌ Not checking page state after actions (use `mcp_microsoft_pla_browser_snapshot`)
- ❌ Forgetting to test data persistence (page refresh)
- ❌ Not testing validation and error cases
- ❌ Leaving browser in inconsistent state (always navigate fresh)

### 8. Terminal Management
- **Keep servers running**: Background process with `isBackground=true`
- **Check output**: Use `get_terminal_output(id)` to verify no errors
- **Close on completion**: Kill terminals after final testing complete
- **Monitor logs**: Watch for exceptions or warnings in output

## Backend Architecture

### Stack & Dependencies
- **Python**: 3.9+
- **Framework**: FastAPI (async web framework)
- **ORM**: SQLAlchemy with SQLite database
- **Database File**: `backend/pingchampions.db` (auto-created on first run)
- **Entry Point**: `backend/main.py` runs on `http://127.0.0.1:8000`

### Key Files Structure
```
backend/
├── main.py              # FastAPI app, CORS setup, router registration
├── database.py          # SQLAlchemy engine, session factory, Base class
├── schemas.py           # Pydantic request/response models (if using)
├── models/
│   ├── __init__.py      # Imports Event, Player, Match (MUST maintain!)
│   ├── event.py         # Event model: name, date (YYYY-MM-DD), time, active flag
│   ├── player.py        # Player model: event_id FK, name, initial_elo
│   └── match.py         # Match model: event_id FK, p1_id, p2_id, winner_id
└── routers/
    ├── events.py        # POST/GET /events/* endpoints
    ├── players.py       # POST/GET /players/* endpoints
    ├── matches.py       # POST/GET /matches/* endpoints
    └── ranking.py       # GET /ranking/* endpoints
```
### Models Relationship Map
```
    Group
      |
      +---> Event (1) ---> (N) Player
             |
             +---> (N) Match
      
Player (1) ---> (N) Match (as player_1)
       (1) ---> (N) Match (as player_2)
```

### Code Conventions
- **Date Format**: Use `YYYY-MM-DD` strings in Event model (NOT DateTime columns)
- **Soft Deletes**: Use `active` boolean flag instead of hard deletes
- **API Response Format**: Return model instances directly (FastAPI auto-serializes)
- **Unicode Output**: Avoid special characters in terminal output (use ASCII-only: [OK], [ERROR], [WARNING])

### File Naming
- JavaScript services: `camelCase.js` (e.g., `api.js`, `events.js`)
- Python modules: `snake_case.py` (e.g., `database.py`, `event.py`)


## Design Decisions

### Why Soft Delete Instead of Hard Delete?
- **Data Preservation**: Audit trail of all events
- **Recovery**: Mistakes are reversible
- **Reporting**: Historical data remains queryable

### Why String Dates in Event Model?
- **Simplicity**: Frontend sends `YYYY-MM-DD` strings, no parsing needed
- **Format Consistency**: All events use same format
- **Note**: This is noted as a potential future refactor (use proper DateTime columns)

## Asking for Clarification

When in doubt about project structure or conventions:
1. Check this file first (answers 90% of setup/workflow questions)
2. Consult `README.md` for high-level architecture
3. Examine existing code in routers/ or views/ for patterns
4. Ask on chat

## Contact & Documentation

- **Project README**: `README.md` (architecture overview, task list reference)
- **Code Comments**: Inline comments in models and routers explain business logic

---

**Last Updated**: Generated from codebase analysis
**Python Version**: 3.9+
**Node Version**: 16.x+ (verified with `node -v`)
**Database**: SQLite (file-based, auto-created)
