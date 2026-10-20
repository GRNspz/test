"""FastAPI application with PostgreSQL persistence for greeting names."""

from fastapi import Depends, FastAPI, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from api.database import get_db_session
from api.models import Greeting

# Create a module-level dependency for the database session
db_dependency = Depends(get_db_session)

app = FastAPI()


# HTML template with form and name history list
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hallo Web App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        .form-group {
            margin: 20px 0;
        }
        input[type="text"] {
            padding: 10px;
            width: 200px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            min-height: 20px;
            background-color: #f8f9fa;
        }
        #history {
            margin-top: 30px;
            text-align: left;
        }
        #history h2 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #333;
        }
        #history ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        #history li {
            padding: 8px 12px;
            border-bottom: 1px solid #eee;
            background-color: #f9f9f9;
            margin-bottom: 5px;
            border-radius: 4px;
        }
        #history li:last-child {
            border-bottom: none;
        }
        .timestamp {
            color: #666;
            font-size: 0.85em;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>Hallo Web App</h1>
    <div class="form-group">
        <form id="nameForm">
            <input type="text" id="name" name="name" placeholder="Dein Name" required>
            <button type="submit">Senden</button>
        </form>
    </div>
    <div id="result"></div>
    <div id="history">
        <h2>Letzte Begrüßungen:</h2>
        <ul id="greetingsList"></ul>
    </div>

    <script>
        // Function to fetch and display greeting history
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const history = await response.json();
                const list = document.getElementById('greetingsList');
                
                if (history.length === 0) {
                    list.innerHTML = '<li>Noch keine Begrüßungen</li>';
                    return;
                }
                
                list.innerHTML = history.map(greeting => 
                    `<li>${greeting.name} <span class="timestamp">(${new Date(greeting.created_at).toLocaleString('de-DE')})</span></li>`
                ).join('');
            } catch (error) {
                console.error('Error loading history:', error);
            }
        }

        // Load history on page load
        document.addEventListener('DOMContentLoaded', loadHistory);

        document.getElementById('nameForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            
            try {
                const response = await fetch('/api/hello', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `name=${encodeURIComponent(name)}`
                });
                
                const result = await response.text();
                document.getElementById('result').textContent = result;
                document.getElementById('name').value = '';
                
                // Reload history after successful submission
                await loadHistory();
            } catch (error) {
                document.getElementById('result').textContent = 'Fehler: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page with form and history."""
    return HTMLResponse(content=HTML_TEMPLATE, status_code=200)


@app.post("/api/hello")
async def hello(
    name: str = Form(default=""),
    db: Session = db_dependency,
) -> PlainTextResponse:
    """
    Handle form submission: store the name and return greeting.

    Creates a new Greeting record with the submitted name and current timestamp.
    """
    # Create and store the greeting
    greeting = Greeting(name=name)
    db.add(greeting)
    db.commit()
    db.refresh(greeting)

    return PlainTextResponse(content=f"Hallo, {name}!")


@app.get("/api/history")
async def get_history(
    db: Session = db_dependency,
) -> list[dict]:
    """
    Return the last 10 greetings, ordered by most recent first.

    Returns a JSON list of greeting objects with name and created_at fields.
    """
    result = db.scalars(
        select(Greeting).order_by(desc(Greeting.created_at), desc(Greeting.id)).limit(10)
    ).all()

    return [{"name": g.name, "created_at": g.created_at.isoformat()} for g in result]
