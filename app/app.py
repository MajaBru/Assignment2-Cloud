from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()

templates = Jinja2Templates(directory="front-end")


# setup mysql connection
def dbconn():
    config = {
        'host': "129.114.27.249",
        'port': "3306",
        'user': "group4",
        'password': "root123",
        'database': "redditdb"
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/users")
async def get_users():
    users = dbconn()
    return JSONResponse(content=users)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

