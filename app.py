import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_conversations")
# def index():
def get_conversations():
    """Conversation History"""
    conversations = mongo.db.conversations.find()
    return render_template("conversations.html", conversations=conversations)
    # return render_template("index.html", )


@app.route("/welcome")
def welcome():
    """Main Page Welcome"""
    return render_template("welcome.html")


@app.route("/topic")
def topic():
    """Topic Dashboard"""
    return render_template("topic.html")


@app.route("/room")
def room():
    """Room"""
    return render_template("room.html")


@app.route("/chat")
def chat():
    """Chat"""
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
