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

# Do we require unable to connect to DB function
# def mono_connect(url):
#     try:# def monfo_connect(url):
# reyun conn#         conn = pymongo.MongClient(url)
#         return conn

# a p   pfig[(SESSION_PERcANENTt]t= FalsoDB: %s") % e


# conn = mongo_connect(MONGO_URI)

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
    """Main Features Page"""
    return redirect(url_for("getfeatures"))


@app.route("/getfeatures")
def getfeatures():
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

#     session["name"] = None
#     return redirect("/")

    # return render_template("register.html", list = LIST)

    # name = request.form.get("first_name", "world")
    # if not name:
    #     return render_template("register.html", message="Missing First Name")

    # if not request.form.get("first_name"):
    #     return render_template("re


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


# @app.route("/chat")
# def chat():
#     """Chat"""
#     return render_template("chat.html")


@app.route("/chatroom", defaults={"activeconv": ""}, methods=["GET", "POST"])
@app.route("/chatroom/<activeconv>", methods=["GET", "POST"])
def chatroom(activeconv):
    """Chat Room"""

    # initiate chat session
    starttime = datetime.now().strftime("%H:%M:%S")

    # render topics from database for selection
    topics = list(mongo.db.topics.find().sort("topic_name", 1))

    # if active chat session active
    # display chat messages and conversation status flash message
    # if 'convId' in session:
    #     activeconv = session.get('convId')

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

    # if active chat session active
    # display chat messages and conversation status flash message
    # if 'convId' in session:
    #     activeconv = session.get('convId')

    # display chat messages for active conversation
    # return redirect(url_for("chatlist", activeconv=activeconv))

    # else:
    # if request.method == "POST":
    # pendlist = get list of pending get_conversations

    # set session[roletype] for moderator
    # mod = mongo.db.users.find_one(
    # {"username": session["user"]})
    # print(mod["roletype"])
    # session["roletype"] = mod["roletype"]

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
            # session['activeconv'] = activeconv["_id"]
            session['convstatus'] = "active"
            session['roletype'] = "moderator"
            # activeconvid = initconvId
            # print(activeconvid)
            return redirect(url_for(
                "chat", activeconv=activeconv))

    return render_template(
        "chatlist.html", activeconv=activeconv, conversations=conversations)

    # return render_template("chatlist.html", pendlist = pendlist)


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

            # msg = [{
            #     "timestamp": now,
            #     "username": username,
            #     "msgtxt": msgtxt
            # }]

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

            # session.pop('activeconv', None)

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
            # if conversation status is done pop session info
            if activeconv["status"] == 'done':
                session.pop('activeconv', None)
                return redirect(url_for("chatlist"))
            return render_template(
                "chat.html", activeconv=activeconv)
    else:
        # if session["roletype"] == "moderator":
        #     print("Display moderator Active Chat")
        #     flash("Active Chat")
        #     print(session['activeconv'])
        #     return render_template(
        #         "chat.html", activeconv=activeconv)
        # else:
        if session["roletype"] == "moderator":
            print("no active chat redirect to chatlist")
            flash("No Active Chat")
            return redirect(url_for("chatlist"))
        # elif session["roletype"] == "user":
            # print("Display Active Chat")
            # print(session['activeconv'])
            # return render_template(
            #     "chat.html", activeconv=activeconv)
            # else:
            # flash("No Active Chat")
            # return redirect(url_for("chatroom"))

        # return render_template(
        #     "chat.html", activeconv=activeconv)
    # if session.get("activeconv") == activeconv:
    #     flash("Active Chat")
    #     print(session['activeconv'])
    #     return render_template(
    #         "chat.html", activeconv=activeconv)


# @app.route("/respond_chat/<convId>", methods=["GET", "POST"])
# def respond_chat(convId):
#     conversation = mongo.db.conversations.find_one(
#         {"_id": ObjectId(convId)})
#     topics = mongo.db.conversations.find().sort("topic_name", 1)
#     return render_template(
#         "respond_chat.html", conversation=conversation, topics=topics)
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
        print("currentcoverid prior to find one " +
              "and update to add message to conversation")
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


# @ app.route("/<username>")
# def user(username):
#     """Display chat message"""
#     return render_template("chat.html", username=username, messages=messages)


# @ app.route("/<username>/<message>")
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
# return render_template("index.html", \
# name=requrest.form.get("first_name", "world"))

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
