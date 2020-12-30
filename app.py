import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

# from flask_session import Session

# __name__ of the current file as a Flask instance
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# LIST = []

# message_history = {}


@app.route("/")
def index():
    """Main Page Welcome"""
    # if not session.get("name"):
    #     return redirect("/login")
    return render_template("welcome.html")


@app.route("/welcome")
def welcome():
    """Main Page Welcome"""
    return render_template("welcome.html")


@ app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""
    return render_template("register.html")


@ app.route("/get_conversations")
# def index():
def get_conversations():
    """Conversation History"""
    conversations = mongo.db.conversations.find()
    return render_template("conversations.html", conversations=conversations)
    # return render_template("index.html", )

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         # store username in session
#         session["name"] = request.form.get("name")
#         return redirect("/")
#     return render_template("login.html")


# @app.route("/logout")
# def logout():
#     session["name"] = None
#     return redirect("/")

    # return render_template("register.html", list = LIST)

    # name = request.form.get("first_name", "world")
    # if not name:
    #     return render_template("register.html", message="Missing First Nme")

    # if not request.form.get("first_name"):
    #     return render_template("register.html", name=request.form.get("first_name", "world"))


@ app.route("/topic")
def topic():
    """Topic Dashboard"""
    return render_template("topic.html")


@ app.route("/room")
def room():
    """Room"""
    return render_template("room.html")


@ app.route("/chat")
def chat():
    """Chat"""
    return render_template("chat.html")


# request arguments and default values
# URL/?name=<value>
# Use POST with form to secure personal data
#
# @app.route("/user", methods=["GET", "POST"])
# def user():
#     return render_template("index.html", name=requrest.form.get("first_name", "world"))
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
