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

# see data in thedatabase
# @app.cli.command('db_seed')
# def db_seed():


# __name__ of the current file as a Flask instance
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/features")
def features():
    """Main Features Page"""
    return redirect(url_for("get_features"))


@app.route("/get_features")
def get_features():
    """Get Features"""
    # get features from database
    features = list(mongo.db.features.find().sort("feature_name", 1))
    # pass featurs to template
    return render_template("features.html", features=features)


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
        # consider customizing the hash and salt methods
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "roletype": "user"}
        mongo.db.users.insert_one(register)

        # capture username for session
        session["user"] = request.form.get("username").lower()
        session["roletype"] = 'user'
        flash("Registration Successful")
        # Redirect to profile page after successful registration
        return redirect(url_for("profile", username=session["user"]))

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
    if request.method == "POST":
        # check to see if user exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                # set session variables
                session["roletype"] = existing_user["roletype"]
                print("Login")
                print(existing_user["roletype"])
                print(session.get("activeconv"))

                # Redirect to profile page after successful registration
                return redirect(url_for(
                    "profile", username=session["user"]))
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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get the session user's name from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/topic")
def topic():
    """Topic Dashboard"""
    return render_template("topics.html")


@app.route("/get_topics")
def get_topics():
    """Get Topics"""
    # get topics form database
    topics = list(mongo.db.topics.find().sort("topic_name", 1))
    # pass topics to template
    return render_template("topics.html", topics=topics)


@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    if request.method == "POST":
        topic = {
            "topic_name": request.form.get("topic_name")
        }
        mongo.db.topics.insert_one(topic)
        flash("New Topic Added")
        return redirect(url_for("get_topics"))

    return render_template("add_topic.html")


@app.route("/edit_topic/<topic_id>", methods=["GET", "POST"])
def edit_topic(topic_id):
    if request.method == "POST":
        submit = {
            "topic_name": request.form.get("topic_name")
        }
        mongo.db.topics.update({"_id": ObjectId(topic_id)}, submit)
        flash("Topic Sucessfully Updated")
        return redirect(url_for("get_topics"))

    topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})
    return render_template("edit_topic.html", topic=topic)


@app.route("/delete_topic/<topic_id>")
def delete_topic(topic_id):
    mongo.db.topics.remove({"_id": ObjectId(topic_id)})
    flash("Topic Successfully Deleted")
    return redirect(url_for("get_topics"))


@ app.route("/room")
def room():
    """Room"""
    return render_template("room.html")


@ app.route("/chatroom", defaults={"activeconv": ""}, methods=["GET", "POST"])
@ app.route("/chatroom/<activeconv>", methods=["GET", "POST"])
def chatroom(activeconv):
    """Chat Room"""

    # initiate chat session
    starttime = datetime.now().strftime("%H:%M:%S")

    # render topics from database for selection
    topics = list(mongo.db.topics.find().sort("topic_name", 1))

    if activeconv != "":
        activeconv = mongo.db.conversations.find_one(
            {"_id": ObjectId(activeconv)})

    if request.method == "POST":
        conversation = {
            "topic_name": request.form.get("topic_name"),
            "username": session["user"],
            "timestamp": starttime,
            "status": "pending"
        }

        # initiate conversation
        initconv = mongo.db.conversations.insert_one(conversation)

        # capture conversationid
        initconvId = initconv.inserted_id

        # custom session variable to capture
        # conversationid and conversation status
        session['activeconv'] = str(initconvId)
        session['convstatus'] = "active"

        activeconv = initconvId

        # print("activeconv: ")
        # print(activeconv)

        flash("Conversation Initiated Pending Moderator")
        return redirect(url_for("chat", activeconv=activeconv))

    return render_template("chatroom.html",
                           topics=topics,
                           activeconv=activeconv)


@app.route("/chatlist", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chatlist/<activeconv>", methods=["GET", "POST"])
def chatlist(activeconv):
    """Chat List"""

    conversations = list(
        mongo.db.conversations.find())
    # display pending chats
    for conversation in conversations:
        initconvId = conversation['_id']
        # print(str(conversation['_id']))
        timestamp = conversation['_id'].generation_time
        # if conversation.status == "pending":
        # print(timestamp)

    # response button function to respond to pending conversation
    # update status and add moderator

    print("Review Chat List")

    if activeconv != "":
        print("Review Chat List")
        # print("session["activeconv"])

        activeconv = mongo.db.conversations.find_one(
            {"_id": ObjectId(activeconv)})

        if activeconv["status"] == "pending":
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(activeconv["_id"])},
                {"$set": {"moderator": session["user"], "status": 'active'}})

            flash("Moderator Responded")
            # custom session variable to capture
            # conversationid and conversation status
            session['activeconv'] = str(initconvId)
            session['convstatus'] = "active"
            session['roletype'] = "moderator"
            print('Moderator Responded (activeconv):' + session["activeconv"])
            return redirect(url_for(
                "chat", activeconv=activeconv))

    return render_template(
        "chatlist.html", activeconv=activeconv, conversations=conversations)


@app.route("/chat", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chat/<activeconv>", methods=["GET", "POST"])
def chat(activeconv):
    """ Chat conversation """
    print("Enter Chat")
    # print(session["activeconv"])

    # capture text messages and update conversation
    if request.method == "POST":
        if request.form['submit_button'] == 'Send':
            print("Send Message")
            print(session["activeconv"])

            msgtime = datetime.now().strftime("%H:%M:%S")

            print(session["activeconv"])
            print(session["user"])
            print(request.form.get("msgtxt"))

            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$push": {"msg": {"timestamp": msgtime,
                                   "username": session["user"],
                                   "msgtxt": request.form.get("msgtxt")}}})

            # pass to chat template for rendering
            activeconvinfo = mongo.db.conversations.find_one(
                {"_id": ObjectId(session["activeconv"])})

            print(activeconvinfo["_id"])

            activeconv = session["activeconv"]

            flash("Message Sent")
            return redirect(url_for("chat", activeconv=activeconv))
        elif request.form['submit_button'] == 'End':
            flash("End Conversation")
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$set": {"status": "done"}})
            # pop session info
            session.pop('activeconv', None)
            if session["roletype"] == "moderator":
                return redirect(url_for("chatlist"))
            else:
                return redirect(url_for("chatroom"))

    if activeconv != "":
        print("Display Active Chat")
        # print(activconv)

        if session["roletype"] == "user" and session['convstatus'] == "active":
            print(session['activeconv'])
            print(session['roletype'])
            print(session['convstatus'])
            # pass to chat template for rendering
            activeconv = mongo.db.conversations.find_one(
                {"_id": ObjectId(session["activeconv"])})
            if activeconv["status"] == 'done':
                # if conversation status is done pop session info
                session.pop('activeconv', None)
                return redirect(url_for("chatroom"))
            return render_template(
                "chat.html", activeconv=activeconv)
        elif (session["roletype"] == "moderator") and (
                session['convstatus'] == "active"):
            activeconv = mongo.db.conversations.find_one(
                {"_id": ObjectId(session["activeconv"])})
            if activeconv["status"] == 'done':
                # if conversation status is done pop session info
                session.pop('activeconv', None)
                return redirect(url_for("chatlist"))
            return render_template(
                "chat.html", activeconv=activeconv)
    else:
        if session["roletype"] == "moderator":
            print("no active chat redirect to chatlist")
            flash("No Active Chat")
            return redirect(url_for("chatlist"))


@app.route("/annotatechats", defaults={"convid": ""}, methods=["GET", "POST"])
@app.route("/annotatechats/<convid>", methods=["GET", "POST"])
def annotatechats(convid):

    # render ratings from database for selection
    ratings = list(mongo.db.ratings.find().sort("rating", 1))

    """Get Completed Chats"""
    # get conversations from database
    conversations = list(mongo.db.conversations.find().sort("topic_name", 1))
    # pass conversation to template
    if session["roletype"] == "annotator":

        if convid == "":
            print("List Conversations for Annotation")
            return render_template("annotatechats.html",
                                   conversations=conversations,
                                   ratings=ratings)
        else:
            # capture rating when button pressed
            if request.method == "POST":
                print("POST Triggered")
                print("before:" + convid)
                if request.form['update_button'] == 'Update':
                    selected_rating = request.form.get("rating_name")
                    print("after:" + convid)
                    print("Rating selected: " + selected_rating)
                    print("Update Conversation")
                    flash("Conversation Annotated")

                    print("before update:" + convid)
                    mongo.db.conversations.find_one_and_update(
                        {"_id": ObjectId(convid)},
                        {"$set": {"status": "annotated",
                                  "rating": request.form.get("rating_name")
                                  }})

                    # mongo.db.conversations.find_one_and_update(
                    #     {"_id": ObjectId(convid)},
                    #     {"$set": {"rating": request.form.get("rating_name")}})

                    # mongo.db.conversations.find_one_and_update(
                    #     {"_id": activeconv},
                    #     {"$set": {"status": 'annotated',
                    #         "rating": request.form.get("rating_name")
                    #     }}
                    # )
               # activeconv = ""
                # if session["roletype"] == "annotator":
                return redirect(url_for("annotatechats"))


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")

    # render ratings from database for selection
    ratings = list(mongo.db.ratings.find().sort("rating", 1))
    # get conversations from database
    conversations = list(mongo.db.conversations.find(
        {"$text": {"$search": query}}))

    return render_template("annotatechats.html",
                           conversations=conversations,
                           ratings=ratings)


@ app.route("/delchat/<delconvid>")
def delchat(delconvid):
    print("delete conversation")
    print(delconvid)
    mongo.db.conversations.remove({"_id": ObjectId(delconvid)})
    flash("Conversation Sucessfully Deleted")
    return redirect(url_for("annotatechats"))


# Custom Error Handling

@ app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# testing 500
# @app.route('/')
# def index():
#     return 1/0


@ app.errorhandler(500)
def internal_server(error):
    return render_template('500.html'), 500


# testing 405
# @app.route('/', methods=["POST"]))
# def index():
#     return "Successful POST request"
# if postman sends a get request it will invoke the 045 error

@ app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
