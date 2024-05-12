from fastapi import FastAPI, Body
import uvicorn
import pymongo


# Database connection + setup
myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
mydb = myclient["mydatabase"]  # Make new database.
mycol = mydb["messages"]  # Make new collection "messages" in the database.


# API
app = FastAPI()


@app.get("/messages")
def read_messages():
    x = mycol.find_one()
    return {"messages": str(x)}


@app.get("/messages/{message_id}")
def read_message(message_id: int):
    myquery = {"message_id": message_id}

    messages = mycol.find(myquery)
    for message in messages:
        return {
            "message_id": message_id,
            "message": str(message)
        }


@app.post("/messages")
def post_message(message: dict = Body(...)):
    x = mycol.insert_one(message)
    return {"message_id": str(x.inserted_id)}


# If ran (not just imported from elsewhere), launch the server.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
