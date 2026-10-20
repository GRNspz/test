# Hallo Web App mit Persistenz

Eine Webapp mit FastAPI, PostgreSQL-Persistenz und HTML-Formular. Die App speichert begrüßte Namen mit Zeitstempel und zeigt die letzten 10 Begrüßungen an.

## Struktur

- `api/main.py` - FastAPI-Anwendung mit Endpunkten
- `api/config.py` - Konfiguration über Umgebungsvariablen (DATABASE_URL)
- `api/database.py` - SQLAlchemy-Datenbank-Verbindungsmanagement
- `api/models.py` - SQLAlchemy-Modell für Greetings
- `alembic/` - Alembic-Migrationen
- `alembic/versions/5c187f790c0b_create_greetings_table.py` - Initial-Migration
- `tests/test_app.py` - pytest-Tests
- `tests/conftest.py` - Test-Fixtures für In-Memory-SQLite
- `vercel.json` - Vercel-Konfiguration für Python-Serverless

## Voraussetzungen

- Python 3.12+
- uv (für Paketmanagement)
- PostgreSQL-Datenbank (für Produktion)

### Abhängigkeiten installieren

```bash
# Alle Abhängigkeiten installieren
uv sync
```

## Lokales Starten

### 1. Umgebungsvariable konfigurieren

Erstelle eine `.env`-Datei im Projektverzeichnis:

```bash
# Beispiel für lokale Entwicklung mit PostgreSQL
echo "DATABASE_URL=postgresql://user:password@localhost:5432/hello_web_app" > .env

# Oder für SQLite (nur für Tests)
echo "DATABASE_URL=sqlite:///./app.db" > .env
```

### 2. Datenbank-Migration ausführen

```bash
# Migrationen gegen die Datenbank ausführen
uv run alembic upgrade head
```

### 3. Anwendung starten

```bash
# Entwicklungsserver starten
uv run uvicorn api.main:app --reload --port 8000

# App ist verfügbar unter: http://localhost:8000
```

## Testen

```bash
# Alle Tests ausführen (verwendet In-Memory-SQLite)
uv run pytest

# Tests mit detaillierter Ausgabe
uv run pytest -v

# Nur spezifische Tests ausführen
uv run pytest tests/test_app.py

# Test mit Code-Coverage
uv run pytest --cov=api tests/
```

## Datenbank-Migrationen

### Neue Migration erstellen

```bash
# Automatisch Migration aus Modellen generieren
uv run alembic revision --autogenerate -m "Beschreibung der Änderung"
```

### Migrationen anwenden

```bash
# Alle ausstehenden Migrationen anwenden
uv run alembic upgrade head
```

### Migrationen zurücksetzen

```bash
# Zur vorherigen Version zurück
uv run alembic downgrade -1

# Zu einer bestimmten Revision zurück
uv run alembic downgrade <revision_id>
```

## Verwendung

1. Öffne die Webseite unter http://localhost:8000
2. Gib deinen Namen im Textfeld ein
3. Klicke auf "Senden"
4. Die Begrüßung "Hallo, <Name>!" wird angezeigt
5. Unter dem Formular wird die Liste der letzten 10 begrüßten Namen angezeigt (neueste zuerst)

## Deployment auf Vercel

1. Repository auf GitHub pushen
2. Bei Vercel ein neues Projekt erstellen
3. GitHub-Repository auswählen
4. Vercel erkennt automatisch die `vercel.json` und deployed die App

### Wichtige Hinweise für Vercel

- Die Datenbankverbindung muss den **Transaction Mode Pooler** verwenden
- **Prepared Statements müssen deaktiviert sein** für PostgreSQL mit Pooler
- Dies ist in `api/database.py` bereits konfiguriert:
  ```python
  connect_args = {"application_name": "hello-web-app"}
  ```
- Die Connection-String sollte so aussehen:
  `postgresql://user:password@aws-1-region.pooler.supabase.com:5432/postgres`

## Projekt-Regeln

- alle Abhängigkeiten werden mit `uv add` verwaltet
- die Datenbank-Konfiguration erfolgt ausschließlich über die Umgebungsvariable `DATABASE_URL`
- die `.env`-Datei bleibt untracked (in .gitignore)
- die Alembic-Migrationen werden im Repo versioniert
- Tests laufen gegen In-Memory-SQLite mit FastAPI Dependency Override
