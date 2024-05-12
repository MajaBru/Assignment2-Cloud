from flask import Flask, request, jsonify
import pymongo


# Database connection + setup
myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
mydb = myclient["mydatabase"]  # Make new database.
mycol = mydb["messages"]  # Make new collection "messages" in the database.


# API
app = Flask(__name__)


@app.route("/messages")
def read_messages():
    x = mycol.find_one()
    return {"messages": str(x)}


@app.route("/messages/{message_id}")
def read_message(message_id: int):
    myquery = {"message_id": message_id}
    messages = mycol.find(myquery)
    return jsonify({
            "message_id": message_id,
            "message": str(message)
        })


@app.route("/messages", methods=["POST"])
def post_message():
    message = request.json
    x = mycol.insert_one(message)
    return jsonify({"message_id": str(x.inserted_id)})

# If ran (not just imported from elsewhere), launch the server.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
