from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("front-end/index.html", "r") as file:
        html_content = file.read()
    return html_content
