from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# HTML template mit Formular
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

    <script>
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
    return HTMLResponse(content=HTML_TEMPLATE, status_code=200)

@app.post("/api/hello")
async def hello(name: str = Form(default="")):
    return PlainTextResponse(content=f"Hallo, {name}!")
