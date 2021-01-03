import os
from datetime import datetime
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


# @app.route("/")
# def index():
#     """Main Page Welcome"""
#     # if not session.get("name"):
#     #     return redirect("/login")
#     return render_template("welcome.html")

@app.route("/")
@app.route("/welcome")
def welcome():
    """Main Page Welcome"""
    return render_template("welcome.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""
    if request.method == "POST":
        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("User Name already exists")
            return redirect(url_for("register"))

        # consider adding secondary password confirmation field
        # consider customizing the hash and slat methods
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # capture username for session
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")

    return render_template("register.html")


@app.route("/get_conversations")
# def index():
def get_conversations():
    """Conversation History"""
    conversations = mongo.db.conversations.find()
    return render_template("conversations.html", conversations=conversations)
    # return render_template("index.html", )


@app.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    #     # store username in session
    #     session["name"] = request.form.get("name")
    #     return redirect("/")
    if request.method == "POST":
        # check to see if user exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

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


# messages = []


# def add_messages(username, message):
#     """Add Messages to messages list"""
#     now = datetime.now().strftime( %H:%M:%S")
#     messages.append("({})) {}: {}".format(now, username, message))


# def get_all_messages():
#     """Get all of the messages and separate then with a 'br'"""
#     return "br".join(messages)


# @app.route("/<username>")
# def user(username):
#     """Display chat message"""
#     return "<h1>Welcome, {0}</h1> {1}".format(username, get_all_messages())


# @app.route("/<username>/,message>")
# def send_message(username, message):
#     """Create a new message and redirect back to the chat page"""
#     add_messages(username, message)
#     return redirect("/" + username)


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
