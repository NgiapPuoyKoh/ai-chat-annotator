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

# Future enhancement: consider seed data in the database
# @app.cli.command('db_seed')
# def db_seed():


# __name__ of the current file as a Flask instance
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Render feature description and where to start
# based on user access role type


@app.route("/")
@app.route("/features")
def features():
    """Main Features Page"""
    return redirect(url_for("get_features"))


# Read Feature description and details steps from database
@app.route("/get_features")
def get_features():
    """Get Features"""
    # get features from database
    features = list(mongo.db.features.find().sort("feature_name", 1))
    # pass featurs to template
    return render_template("features.html", features=features)


# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""
    if request.method == "POST":

        username = request.form.get("username").lower()

        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"username": username})

        if existing_user:
            flash("User Name already exists")
            return redirect(url_for("register"))

        # Future Enhancements
        # consider adding secondary password confirmation field
        # consider customizing the hash and salt methods
        register = {
            "username": username,
            "password": generate_password_hash(request.form.get("password")),
            "roletype": "user"}
        mongo.db.users.insert_one(register)

        # capture username for session
        session["user"] = username
        session["roletype"] = 'user'
        flash("Registration Successful")
        # Redirect to profile page after successful registration
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# User Login utilized hash passwords
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username").lower()

        # check to see if user exists in db
        existing_user = mongo.db.users.find_one(
            {"username": username})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = username
                flash("Welcome, {}".format(username))
                # set session variables
                session["roletype"] = existing_user["roletype"]
                # log session info
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


# User Logout
@app.route("/logout")
def logout():

    # If not user in session Redirect to Features
    if 'user' not in session:
        flash("You are currently not logged in")
        return redirect(url_for('features'))

    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("features"))


# Read Session User Profile Name from database
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    if 'user' in session:
        # get the session user's name from the database
        username = mongo.db.users.find_one_or_404(
            {"username": session["user"]})["username"]
        return render_template("profile.html", username=username)
    else:
        flash('No active session')
        return redirect(url_for("login"))


# Render topic dashboard
@app.route("/topic")
def topic():
    """Topic Dashboard"""
    if ('user' in session) and (
        'roletype' in session) and (
            session['roletype'] == 'admin'):
        return render_template("topics.html")
    flash("You do not have privileges to Access Topics")
    return redirect(url_for("features"))


# Read topics from database
@app.route("/get_topics")
def get_topics():
    """Get Topics"""
    if 'user' in session and (
        'roletype' in session) and (
            session['roletype'] == 'admin'):
        # get topics from database
        topics = list(mongo.db.topics.find().sort("topic_name", 1))
        # pass topics to template
        return render_template("topics.html", topics=topics)
    flash("You do not have privileges to Access Topics")
    return redirect(url_for("features"))


# Create new topic
@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    """ Add Topic """
    if ('user' in session) and (
        'roletype' in session) and (
            session['roletype'] == 'admin'):
        if request.method == "POST":
            topic = {
                "topic_name": request.form.get("topic_name")
            }
            mongo.db.topics.insert_one(topic)
            flash("New Topic Added")
            return redirect(url_for("get_topics"))
        return render_template("add_topic.html")
    flash("You do not have privileges to Add Topic")
    return redirect(url_for("features"))


# Update topic
@app.route("/edit_topic/<topic_id>", methods=["GET", "POST"])
def edit_topic(topic_id):
    """ Edit Topic """
    if ('user' in session) and (
        'roletype' in session) and (
            session['roletype'] == 'admin'):
        if request.method == "POST":
            submit = {
                "topic_name": request.form.get("topic_name")
            }
            mongo.db.topics.update({"_id": ObjectId(topic_id)}, submit)
            flash("Topic Sucessfully Updated")
            return redirect(url_for("get_topics"))

        if request.method == "GET":
            print(topic_id)
            if ObjectId.is_valid(topic_id):
                topic = mongo.db.topics.find_one({"_id": ObjectId(topic_id)})
                return render_template("edit_topic.html", topic=topic)
            # if topic id is invalid valid else return a 404
            else:
                return render_template('404.html'), 404
    flash("You do not have privileges to Edit Topic")
    return redirect(url_for("features"))


# Delete topic from database
@app.route("/delete_topic/<topic_id>")
def delete_topic(topic_id):
    """ Delete Topic """
    if ('user' in session) and (
        'roletype' in session) and (
            session['roletype'] == 'admin'):
        mongo.db.topics.remove({"_id": ObjectId(topic_id)})
        flash("Topic Successfully Deleted")
        return redirect(url_for("get_topics"))
    flash("You do not have privileges to Delete Topic")
    return redirect(url_for("features"))


# Chatroom where User selects a topic and
# initiatie and engages in active conversation
# Create conversations and insert messages into database
@app.route("/chatroom", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chatroom/<activeconv>", methods=["GET", "POST"])
def chatroom(activeconv):
    """Chat Room"""

    # If not user in session Redirect to Features
    if 'user' not in session:
        flash("You are currently not logged in")
        return redirect(url_for('features'))

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

        # set up parameter for redirect
        activeconv = initconvId

        flash("Conversation Initiated Pending Moderator")
        return redirect(url_for("chat", activeconv=activeconv))

    return render_template("chatroom.html",
                           topics=topics,
                           activeconv=activeconv)


# Chatlist for moderator response to user initiated conversations
@app.route("/chatlist", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chatlist/<activeconv>", methods=["GET", "POST"])
def chatlist(activeconv):
    """Chat List"""

    conversations = list(
        mongo.db.conversations.find())
    # get chats for chatlist to display pending and active chats
    initconvId = conversations[len(conversations)-1]['_id']

    # response button function to respond to pending conversation
    # update status and add moderator
    if activeconv != "":
        print("Review Chat List")

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


# Display active conversation with messages
@app.route("/chat", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chat/<activeconv>", methods=["GET", "POST"])
def chat(activeconv):
    """ Chat conversation """

    # If not user in session Redirect to Features
    if 'user' not in session:
        flash("You are currently not logged in")
        return redirect(url_for('features'))

    # capture text messages and update conversation
    if request.method == "POST":
        if request.form['submit_button'] == 'Send':
            # time stamp
            msgtime = datetime.now().strftime("%H:%M:%S")

            # log session info
            print(session["activeconv"])
            print(session["user"])
            print(request.form.get("msgtxt"))

            # insert message to conversation
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$push": {"msg": {"timestamp": msgtime,
                                   "username": session["user"],
                                   "msgtxt": request.form.get("msgtxt")}}})

            # pass to chat template for rendering
            activeconvinfo = mongo.db.conversations.find_one(
                {"_id": ObjectId(session["activeconv"])})

            # log active conversatin info
            print(activeconvinfo["_id"])

            activeconv = session["activeconv"]

            flash("Message Sent")
            return redirect(url_for("chat", activeconv=activeconv))
        # user or moderator ends conversation
        elif request.form['submit_button'] == 'End':

            # time stamp
            msgtime = datetime.now().strftime("%H:%M:%S")

            # capture message text and set status
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$push": {"msg": {"timestamp": msgtime,
                                   "username": session["user"],
                                   "msgtxt": request.form.get("msgtxt")}},
                 "$set": {"status": "done"}})

            # Redirect and flash message for ended conversation
            if session["roletype"] == "moderator":
                flash("Ended Conversation")
                return redirect(url_for("chatlist"))
            else:
                flash("Ended Conversation")
                return redirect(url_for("chatroom"))

            # pop session info
            session.pop('activeconv', None)

    # Active conversation in progress
    if activeconv != "":
        print("Display Active Chat")
        # print(activconv)

        if session["roletype"] == "user" and session['convstatus'] == "active":
            # log session info
            print(session['activeconv'])
            print(session['roletype'])
            print(session['convstatus'])
            # pass to chat template for rendering
            activeconv = mongo.db.conversations.find_one(
                {"_id": ObjectId(session["activeconv"])})
            if activeconv["status"] == 'done':
                flash("Ended Conversation")
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
                flash("Ended Conversation")
                # if conversation status is done pop session info
                session.pop('activeconv', None)
                return redirect(url_for("chatlist"))
            return render_template(
                "chat.html", activeconv=activeconv)
    else:
        # handle no pending chats
        if session["roletype"] == "moderator":
            print("no active chat redirect to chatlist")
            flash("No Active Chat")
            return redirect(url_for("chatlist"))


# Annotate Chats
@app.route("/annotatechats", defaults={"convid": ""}, methods=["GET", "POST"])
@app.route("/annotatechats/<convid>", methods=["GET", "POST"])
def annotatechats(convid):

    # If not user in session Redirect to Features
    if 'user' not in session:
        flash("You are currently not logged in")
        return redirect(url_for('features'))

    if ('user' in session) and (
            'roletype' in session) and (
                session['roletype'] == 'annotator'):

        # render ratings from database for selection
        ratings = list(mongo.db.ratings.find().sort("rating", 1))

        """Get Completed Chats"""
        # get conversations from database
        conversations = list(mongo.db.conversations.find().sort(
            "topic_name", 1))
        # pass conversation to template
        if session["roletype"] == "annotator":

            if convid == "":
                print("List Conversations for Annotation")
                return render_template(
                    "annotatechats.html",
                    conversations=conversations,
                    ratings=ratings)
            else:
                # capture rating when button pressed
                if request.method == "POST":
                    # log POST triggered
                    print("POST Triggered")
                    print("before:" + convid)
                    rating_name = request.form.get("rating_name")
                    if request.form['update_button'] == 'Update':
                        print("after:" + convid)
                        print("Rating selected: " + rating_name)
                        print("Update Conversation")
                        flash("Conversation Annotated")
                        # log before update
                        print("before update:" + convid)
                        mongo.db.conversations.find_one_and_update(
                            {"_id": ObjectId(convid)},
                            {"$set": {"status": "annotated",
                                      "rating": rating_name
                                      }})
                    return redirect(url_for("annotatechats"))
    flash("You do not have privileges to Annotate Chats")
    return redirect(url_for("features"))


# Search Conversations by Topic Name for Annotation
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


# Delete Conversation
@app.route("/delchat/<delconvid>")
def delchat(delconvid):
    # log delete conversation
    print("delete conversation")
    print(delconvid)
    mongo.db.conversations.remove({"_id": ObjectId(delconvid)})
    flash("Conversation Successfully Deleted")
    return redirect(url_for("annotatechats"))


# Custom Error Handling
# 404 Error Page not found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 500 Error Server Error


@app.errorhandler(500)
def internal_server(error):
    return render_template('500.html'), 500

# 405 Error Method


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
