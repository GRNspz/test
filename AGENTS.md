# Projekt-Regeln für Agents

## Arbeitsweise
- Zu Beginn jeder Session: git pull, dann einen Feature-Branch
  feature/<thema> erstellen und ausschließlich darauf arbeiten.
- Niemals direkt auf main committen oder pushen.

## Abhängigkeiten
- Abhängigkeiten ausschließlich mit "uv add <paket>".
- Niemals "uv pip install" oder "pip install" – alles muss in
  pyproject.toml und uv.lock landen.
- Umgebung und Tests laufen über "uv run" (z. B. "uv run pytest").

## Tests & Commits
- Nur committen, wenn alle Tests grün sind.
- Commit-Messages kurz, imperativ, eine Zeile.
- Jeder Commit endet (nach einer Leerzeile) mit:
  Co-authored-by: Vibe Agent <devstral@noreply.mistral.ai>

## Geheimnisse & Deployment
- Niemals .env-Dateien, Keys oder Credentials committen 
  (dieses Repo ist öffentlich!).
- Deploy-Ziel ist Vercel (Python-Serverless): Struktur entsprechend
  aufbauen (z. B. api/-Verzeichnis, vercel.json falls nötig), damit
  der Merge auf main ohne Anpassungen deployt.
- Bei SQLAlchemy mit dem Transaction-Mode-Pooler: prepared statements deaktivieren.