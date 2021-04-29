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


# Read and reder Feature description and details steps from database
@app.route("/")
@app.route("/get_features")
def get_features():
    """Get Features"""
    app.logger.info('Current after login session=%s', session)
    # get features from database
    features = list(mongo.db.features.find().sort("feature_name", 1))
    # pass featurs to template
    return render_template("features.html", features=features)


# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""

    if is_authenticated():
        flash("Please Logout First to execute this operation")
        redirect(url_for("get_features"))

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
    if is_authenticated():
        flash("Please Logout First to excute this operation")
        redirect(url_for("get_features"))

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

                app.logger.info('Current after login session=%s', session)

                # Redirect to features page after successful registration
                return redirect(url_for("get_features"))
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
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for('get_features'))

    # remove user from session cookies
    flash("You have been logged out")
    session.pop('user')
    session.pop('roletype')

    remove_conversation_from_session()

    app.logger.info('Current after logout session=%s', session)

    return redirect(url_for("get_features"))


# Read Session User Profile Name from database
@app.route("/profile", methods=["GET"])
def profile():
    if is_authenticated():
        # get the session user's name from the database
        username = mongo.db.users.find_one_or_404(
            {"username": session["user"]})["username"]
        return render_template("profile.html", username=username)
    else:
        flash('You are currently not logged in')
        return redirect(url_for("login"))


# Read topics from database and render topic dashboard
@app.route("/get_topics")
def get_topics():
    """Get Topics"""
    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for('get_features'))

    if is_admin():
        # get topics from database
        topics = list(mongo.db.topics.find().sort("topic_name", 1))
        # pass topics to template
        return render_template("topics.html", topics=topics)
    flash("You do not have privileges to Access Topics")
    return redirect(url_for("get_features"))


# Create new topic
@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    """ Add Topic """
    if is_admin():
        if request.method == "POST":
            topic = {
                "topic_name": request.form.get("topic_name")
            }
            mongo.db.topics.insert_one(topic)
            flash("New Topic Added")
            return redirect(url_for("get_topics"))
        return render_template("add_topic.html")
    flash("You do not have privileges to Add Topic")
    return redirect(url_for("get_features"))


# Update topic
@app.route("/edit_topic/<topic_id>", methods=["GET", "POST"])
def edit_topic(topic_id):
    """ Edit Topic """
    if is_admin():
        if is_object_id_valid(topic_id):
            topic = mongo.db.topics.find_one_or_404(
                {"_id": ObjectId(topic_id)})
            if request.method == "POST":
                submit = {
                    "topic_name": request.form.get("topic_name")
                }
                mongo.db.topics.update({"_id": ObjectId(topic_id)}, submit)
                flash("Topic Sucessfully Updated")
                return redirect(url_for("get_topics"))

            if request.method == "GET":
                return render_template("edit_topic.html", topic=topic)
        # if topic id is invalid valid else return a 404
        else:
            return render_template('404.html'), 404
    flash("You do not have privileges to Edit Topic")
    return redirect(url_for("get_features"))


# Delete topic from database
@app.route("/delete_topic/<topic_id>")
def delete_topic(topic_id):
    """ Delete Topic """
    if is_admin():
        if is_object_id_valid(topic_id):
            mongo.db.topics.find_one_or_404({"_id": ObjectId(topic_id)})
            mongo.db.topics.remove({"_id": ObjectId(topic_id)})
            flash("Topic Successfully Deleted")
            return redirect(url_for("get_topics"))
    flash("You do not have privileges to Delete Topic")
    return redirect(url_for("get_features"))


# Chatroom where User selects a topic and
# initiatie and engages in active conversation
# Create conversations and insert messages into database
@app.route("/chatroom/", methods=["GET", "POST"])
def chatroom():
    """Chat Room"""

    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for('get_features'))

    # initiate chat session
    starttime = datetime.now().strftime("%H:%M:%S")

    # render topics from database for selection
    topics = list(mongo.db.topics.find().sort("topic_name", 1))

    if request.method == "POST":
        conversation = {
            "topic_name": request.form.get("topic_name"),
            "username": session["user"],
            "moderator": None,
            "timestamp": starttime,
            "status": "pending"
        }

        # initiate conversation
        initconv = mongo.db.conversations.insert_one(conversation)

        # capture conversationid
        activeconv = initconv.inserted_id

        # custom session variable to capture
        # conversationid and conversation status
        session["activeconv"] = str(activeconv)
        session["convstatus"] = "active"

        flash("Conversation Initiated Pending Moderator")
        return redirect(url_for("chat"))

    return render_template("chatroom.html", topics=topics)


# Chatlist for moderator response to user initiated conversations
@app.route("/chatlist", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chatlist/<activeconv>", methods=["GET", "POST"])
def chatlist(activeconv):
    """Chat List"""

    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for('get_features'))

    if is_user_roletype('moderator'):
        conversations = list(mongo.db.conversations.find())
        # get chats for chatlist to display pending and active chats
        initconv_id = conversations[len(conversations)-1]['_id']

        # response button function to respond to pending conversation
        # update status and add moderator
        if is_object_id_valid(activeconv):
            # get conversation id f selected conversation
            activeconv = mongo.db.conversations.find_one(
                {"_id": ObjectId(activeconv)})
            # update conversation
            if activeconv["status"] == "pending":
                mongo.db.conversations.find_one_and_update(
                    {
                        "_id": ObjectId(activeconv["_id"]),
                    },
                    {
                        "$set": {
                            "moderator": session["user"],
                            "status": 'active'
                        }
                    })
                flash("Moderator Responded")
                # custom session variable to capture
                # conversationid and conversation status
                session["activeconv"] = str(initconv_id)
                session["convstatus"] = "active"
                session["roletype"] = "moderator"
                return redirect(url_for("chat"))
        return render_template(
            "chatlist.html", activeconv=activeconv,
            conversations=conversations)
    else:
        flash("You do not have privileges to Annotate")
        return redirect(url_for("get_features"))


# Display active conversation with messages
@app.route("/chat", methods=["GET", "POST"])
def chat():
    """ Chat conversation """

    app.logger.info('Current session=%s', session)

    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for("get_features"))

    # app.pyredirect based on role type
    if 'activeconv' not in session:
        flash("No Active Chat")
        if is_user_roletype("user"):
            return redirect(url_for("chatroom"))
        elif is_user_roletype("moderator"):
            return redirect(url_for("chatlist"))
        elif is_user_roletype("annotator"):
            return redirect(url_for("annotatechats"))
        else:
            return redirect(url_for("get_topics"))

    # capture active conversation id
    activeconv = session["activeconv"]
    if is_user_roletype("moderator"):
        filter = {
            "_id": ObjectId(activeconv),
            "moderator": session["user"]
        }
    elif is_user_roletype("user"):
        filter = {
            "_id": ObjectId(activeconv),
            "username": session["user"]
        }

    # capture text messages and update conversation
    if request.method == "POST":
        # construct the filter
        if request.form['submit_button'] == 'Send':
            # time stamp
            msgtime = datetime.now().strftime("%H:%M:%S")
            # insert message to conversation
            mongo.db.conversations.find_one_and_update(
                filter,
                {
                    "$push": {
                        "msg": {
                            "timestamp": msgtime,
                            "username": session["user"],
                            "msgtxt": request.form.get("msgtxt")
                        }
                    }
                })
            # pass to chat template for rendering
            # activeconvinfo = mongo.db.conversations.find_one(
            #     {"_id": ObjectId(activeconv)})
            flash("Message Sent")
            return redirect(url_for("chat"))
        # user or moderator ends conversation
        elif request.form['submit_button'] == 'End':
            # time stamp
            msgtime = datetime.now().strftime("%H:%M:%S")
            # capture message text and set status
            mongo.db.conversations.find_one_and_update(
                filter,
                {
                    "$push": {
                        "msg": {
                            "timestamp": msgtime,
                            "username": session["user"],
                            "msgtxt": request.form.get("msgtxt")
                        }
                    },
                    "$set": {
                        "status": "done"
                    }
                })
            # pop session info
            remove_conversation_from_session()
            # Redirect and flash message for ended conversation
            if is_user_roletype("moderator"):
                flash("Ended Conversation")
                return redirect(url_for("chatlist"))
            else:
                flash("Ended Conversation")
                return redirect(url_for("chatroom"))

    # Active conversation in progress
    if ('convstatus' in session) and (session["convstatus"] == "active"):
        app.logger.info('Current session=%s', session)
        # pass to chat template for rendering
        activeconv = mongo.db.conversations.find_one_or_404(filter)
        if activeconv["status"] == 'done':
            # if conversation status is done pop session info
            remove_conversation_from_session()
            if is_user_roletype("moderator"):
                flash("Ended Conversation")
                return redirect(url_for("chatlist"))
            else:
                flash("Ended Conversation")
                return redirect(url_for("chatroom"))
        return render_template("chat.html", activeconv=activeconv)
    else:
        flash("No Active Chat Session")
        return redirect(url_for("chatlist"))


# Annotate Chats
@app.route("/annotatechats", defaults={"convid": ""}, methods=["GET", "POST"])
@app.route("/annotatechats/<convid>", methods=["GET", "POST"])
def annotatechats(convid):

    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for("get_features"))

    if is_user_roletype('annotator'):
        # render ratings from database for selection
        ratings = list(mongo.db.ratings.find().sort("rating", 1))

        """Get Completed Chats"""
        # get conversations from database
        conversations = list(mongo.db.conversations.find().sort(
            "topic_name", 1))
        # pass conversation to template
        if convid == "":
            # List Conversations for Annotation
            return render_template(
                "annotatechats.html",
                conversations=conversations,
                ratings=ratings)
        else:
            # capture rating when button pressed
            if request.method == "POST":
                rating_name = request.form.get("rating_name")
                if request.form['update_button'] == 'Update':
                    flash("Conversation Annotated")
                    # update conversation with rating
                    mongo.db.conversations.find_one_and_update(
                        {"_id": ObjectId(convid)},
                        {"$set": {
                            "status": "annotated",
                            "rating": rating_name
                        }}
                    )
                return redirect(url_for("annotatechats"))
    flash("You do not have privileges to Annotate Chats")
    return redirect(url_for("get_features"))


# Search Conversations by Topic Name for Annotation
@app.route("/search", methods=["GET", "POST"])
def search():
    # If not user in session Redirect to Features
    if not is_authenticated():
        flash("You are currently not logged in")
        return redirect(url_for("get_features"))

    if is_user_roletype('annotator'):
        query = request.form.get("query")
        # render ratings from database for selection
        ratings = list(mongo.db.ratings.find().sort("rating", 1))
        # get conversations from database
        conversations = list(mongo.db.conversations.find(
            {"$text": {"$search": query}}))

        return render_template("annotatechats.html",
                               conversations=conversations,
                               ratings=ratings)
    else:
        flash("You do not have privileges to Annotate conversations")
        return redirect(url_for("get_features"))


# Delete Conversation
@app.route("/delchat/<delconvid>")
def delchat(delconvid):
    if is_user_roletype('annotator') and is_object_id_valid(delconvid):
        # delete conversation
        mongo.db.conversations.find_one_or_404({"_id": ObjectId(delconvid)})
        mongo.db.conversations.remove({"_id": ObjectId(delconvid)})
        flash("Conversation Successfully Deleted")
        return redirect(url_for("annotatechats"))
    flash("You do not have privileges to Delete conversations")
    return redirect(url_for("get_features"))


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


def is_object_id_valid(id_value):
    """ Validate is the id_value is a valid ObjectId
    """
    return id_value != "" and ObjectId.is_valid(id_value)


def is_authenticated():
    """ Ensure that user is authenticated
    """
    return 'user' in session


def get_user_role():
    """ Retrieve the user role from session
    """
    if 'roletype' in session:
        return session['roletype']
    return None


def is_user_roletype(roletype):
    """
    Checks if the user is authenticated and the role is the expected
    passed in the parameter roletype.
    """
    return is_authenticated() and get_user_role() == roletype


def is_admin():
    """ Check if the current session user has the `admin` role.
    """
    return is_authenticated() and get_user_role() == 'admin'


def remove_conversation_from_session():
    """ Remove keys and values related to the conversation from session
    """
    if 'convstatus' in session:
        session.pop('convstatus', None)
    if 'activeconv' in session:
        session.pop('activeconv', None)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=False)
