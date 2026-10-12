# Hallo Web App

Eine minimale Webapp mit FastAPI und HTML-Formular.

## Struktur

- `api/main.py` - FastAPI-Anwendung mit Endpunkt
- `vercel.json` - Vercel-Konfiguration für Python-Serverless
- `tests/test_app.py` - pytest-Tests

## Lokales Starten

```bash
# Entwicklungsserver starten
uv run uvicorn api.main:app --reload --port 8000

# App ist verfügbar unter: http://localhost:8000
```

## Testen

```bash
# Alle Tests ausführen
uv run pytest

# Tests mit detaillierter Ausgabe
uv run pytest -v

# Nur spezifische Tests ausführen
uv run pytest tests/test_app.py
```

## Deployment auf Vercel

1. Repository auf GitHub pushen
2. Bei Vercel ein neues Projekt erstellen
3. GitHub-Repository auswählen
4. Vercel erkennt automatisch die `vercel.json` und deployed die App

## Verwendung

1. Öffne die Webseite
2. Gib deinen Namen im Textfeld ein
3. Klicke auf "Senden"
4. Die Begrüßung "Hallo, <Name>!" wird angezeigt
