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
        # consider customizing the hash and salt methods
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # capture username for session
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        # TO DO! Redirect to another page after successful registration!

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
    #     return render_template("register.html", message="Missing First Name")

    # if not request.form.get("first_name"):
    #     return render_template("register.html", name=request.form.get("first_name", "world"))


@app.route("/topic")
def topic():
    """Topic Dashboard"""
    return render_template("topics.html")


@app.route("/gettopics")
def gettopics():
    """Get Topics"""
    # get topics form database
    topics = list(mongo.db.topics.find().sort("topic_name", 1))
    # pass topics to template
    return render_template("topics.html", topics=topics)


@app.route("/room")
def room():
    """Room"""
    return render_template("room.html")


@app.route("/chat")
def chat():
    """Chat"""
    return render_template("chat.html")


@app.route("/chatroom", methods=["GET", "POST"])
def chatroom():
    """Chat Room"""

    # initiate chat session
    starttime = datetime.now().strftime("%H:%M:%S")

    # render topics from database for selection
    topics = list(mongo.db.topics.find().sort("topic_name", 1))

    if request.method == "POST":
        conversation = {
            "topic_name": request.form.get("topic_name"),
            "username": session["user"],
            "timestamp": starttime
        }

        # initiate conversation
        initconv = mongo.db.conversations.insert_one(conversation)

        # capture conversationid
        initconvId = initconv.inserted_id
        print(initconvId)

        flash("Conversation Initiated Pending Moderator")
        return redirect(url_for("chatroom"))

    return render_template("chatroom.html", topics=topics)


# initial session message array display for all users to see
# need to refactor as private messages between user/moderator
messages = []


def add_messages(username, message):
    """Add Messages to messages list"""
    now = datetime.now().strftime("%H:%M:%S")

    # session message display structure
    messages_display = {
        "timestamp": now,
        "username": username,
        "message": [message]
    }

    # db conversation first message structure
    # messages_dict = {
    #     "timestamp": now,
    #     "username": username,
    #     "message": [message]
    # }

    messages_dict_new = {
        "msgstarttime": now,
        "username": username,
        "msg": [{
            "timestamp": now,
            "username": username,
            "msgtxt": message
        }]
    }

    # messages_dict_add = {
    #     "timestamp": now,
    #     "username": username,
    #     "msgtxt": message
    # }
    # print(messages_dict_add)

    # messages_dict_add = {
    #     "msg": [{
    #         "timestamp": now,
    #         "username": username,
    #         "msgtxt": message
    #     }]
    # }
    # print(messages_dict_add)

    # Append message to session messages dict for display
    messages.append(messages_display)

    print(len(messages))
    print(messages)

    # If new conversation Create New conversation session
    if len(messages) == 1:
        # create msg in db
        msgId = mongo.db.conversations.insert_one(messages_dict_new)
        # print(msgId.inserted_id)
        # append msgID to session message dict
        messages.append({"conversationid": msgId.inserted_id})
        # print(messages.conversationid)

        # create chat session with captured new conversation id
        newchatsession = {
            "conversationid": msgId.inserted_id,
            "converstarttime": now,
            "converstatus": "true",
            "user": username
        }

        chatId = mongo.db.chatsessions.insert_one(newchatsession)
        print(chatId.inserted_id)

        print(messages[1])

    # active chat session subsequent messages
    elif len(messages) >= 1:
        # capture subsequent messages in conversation
        # get current conversation id
        print(len(messages))
        print(messages)

        currentconverid = messages[1]["conversationid"]
        print(currentconverid)
        print("currentconverid datatype: ")
        print(type(currentconverid))

        # Test add /update moderator to chat session
        mongo.db.chatsessions.find_one_and_update(
            {"conversationid": ObjectId('60023df6aa00ecf69a2bb599')},
            {"$set": {"moderator": username}})

        # Test add message dict to conversation
        # mongo.db.conversations.find_one_and_update(
        #     {"_id": ObjectId('60023df6aa00ecf69a2bb599')},
        #     {"$push": {"message": messages_dict["message"]}})

        # Test add message to element array of conversation
        mongo.db.conversations.find_one_and_update(
            {"_id": ObjectId('6004a0152b26c9e08a93bee8')},
            {"$push": {"msg": {"timestamp": now,
                               "username": username,
                               "msgtxt": message}
                       }})

        # test messages for conversation are captured in global messages array
        for messageprt in messages:
            print(messageprt)

        # my_document = mongo.db.collection.find_one({"my_property": my_value})
        # email_address = my_document["emailaddress"]

        # when moderator respond add moderator username to chatsession
        # convert cursor of objects/records from Mongo into a Python list
        userrole = list(mongo.db.users.find({"username": username}))
        # print(userrole)

        # get the roletype of the user
        for user.items in userrole:
            print(user.items["roletype"])

        # if moderator first response to active chat session
        # add moderator to user session
        if user.items["roletype"] == "moderator":
            print(user.items["roletype"])

            print("moderator first response to chat")

            print(messages)

            print("currentcoverid prior to add moderator to chatsession")
            print(currentconverid)

            # update or add moderator to active chat session
            mongo.db.chatsessions.find_one_and_update(
                {"conversationid": currentconverid},
                {"$set": {"moderator": username}})

        # test get current conversationid
        testchat = mongo.db.conversations.find_one(
            {"_id": ObjectId('6004a0152b26c9e08a93bee8')}
        )
        print("testchat: ")
        print(testchat)

        # Add messages to conversation
        # current conversation

        activechat = mongo.db.conversations.find_one(
            {"_id": currentconverid})

        print("activechat: ")
        print(activechat)

        # # add message to global message dictionary object
        # messages.append({"timestamp": now,
        #                  "username": username,
        #                  "msgtxt": message})

        # print(messages_dict_add)
        print("currentcoverid prior to find one and update to add message to conversation")
        print(currentconverid)

        mongo.db.conversations.find_one_and_update(
            {"_id": currentconverid},
            {"$push": {"msg": {"timestamp": now,
                               "username": username,
                               "msgtxt": message}}})

        # test add message to chatsession
        # mongo.db.chatsessions.find_one_and_update(
        #     {"conversationid": '60023df6aa00ecf69a2bb599'},
        #     {"$set": {"moderator": username}})

        # get the roletype of the user
        # for chatsessions.items in activechat:
        #     print(user.items["conversationid"])

        # if chatsessions.items["conversationid"] == currentconverid:
        #     print(user.items["conversationid"])

        # get active conversation id
        # if activechat != None:
        # Add moderator to chatsession

        # print(currentconverid)

        # mongo.db.chatsessions.find_one_and_update(
        #     {"conversationid": currentconverid},
        #     {"$set": {"moderator": username}})

        # if active chatsession with converstaionid and converstatus is true
        # mongo.db.conversations.find_one_and_update(
        #     {"_id": currentconverid},
        #     {"$addToSet": {"msg": messages_dict}})

        # find  mongo.db.conversations with
        # _id = "conversationid"
        # "msgstarttime" eqaul "converstarttime"
        # and "converstatus": "true"
        # mongo.db.conversations.find({id: {$gt: 4}})

        #     newchatsession = {
        #         "conversationid": msgId.inserted_id,
        #         "converstarttime": now,
        #         "converstatus": "true"
        #     }
        # then append
        # to conversation with _id = "conversationid"

        #     mongo.db.conversations.find_one_and_update(
        #         {"_id": ObjectId(msgId)},
        #         {"$addToSet": {"msg": messages_dict_add}}

        # When session end set conversation to false

        # Tony = mongo.db.people.update({"_id": ObjectId(hub_mother_id)}, { "$addToSet": {"children": hub_person_id }})

        # for x in mongo.db.conversations.find({}, {"_id": 1, "timestamp": 1}):
        # return msgId

        # mongo.db.conversations.find_one_and_update(
        #     {"_id": ObjectId(msgId)},
        #     {"$addToSet": {"msg": messages_dict}})

        # Tony = mongo.db.people.update({"_id": ObjectId(hub_mother_id)}, { "$addToSet": {"children": hub_person_id }})
        # mongo.db.conversations.countDocuments({})
        # db.orders.countDocuments({})
        # conversation_id = conversation.inserted_id
        # mongo.db.conversations.update_one(messages_dict)
        # messages.append("({})) {}: {}".format(now, username, message))

        # def capture_conversation(messages, topic_name):
        #     """ Add conversation to db"""
        #     # when conversation is terminated user is logout
        #     conversation = {
        #         "topic_name": topic_name,
        #         "rating": "null",
        #         "annotated_status": "Pending",
        #         "messages": messages
        #     }
        # mongo.db.conversations.insert_one(conversation)

        # def get_all_messages():
        #     """Get all of the messages and separate then with a 'br'"""
        #     return "br".join(messages)


@app.route("/<username>")
def user(username):
    """Display chat message"""
    return render_template("chat.html", username=username, messages=messages)


@app.route("/<username>/<message>")
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    add_messages(username, message)
    return redirect("/" + username)


# request arguments and default values
# URL/?name=<value>
# Use POST with form to secure personal data
#
# @app.route("/user", methods=["GET", "POST"])
# def user():
# return render_template("index.html", \
# name=requrest.form.get("first_name", "world"))

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
