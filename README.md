# <h1 align="center">Chat with Conversation Annotator for Chatbot </h1>

[View the live project here.](http://flask-ai-chat-annotate.herokuapp.com/)

This is a chat application interface with a conversation data annotation feature. It is designed to capture actual conversations via the chatbot with annotation to improve the accuracy and quality of the bot conversations.

Data annotators will have access to annotate chat conversations for training AI chatbot for greater accuracy of Chatbot conversations

This application is intended to be lightweight, low maintenance, easy to implement and, easy to use. It enables a business to collect conversations as part of its services operations.

The goal is to provide a tool for actualizing a digital transformation strategy that includes implementing AI and chatbots to optimize operations.

<h2 align="center"><img src="https://thumbs.dreamstime.com/b/chatbot-icon-virtual-assistant-vector-143083940.jpg" alt="chatbot Icon" width=200" height="200"></h2>

## Operational Features

A chat application with conversation data prep to feed into an AI model (not included in the scope)

- Build a real-time chat application (chat room if not too complex) for one on one conversations
- Using Flask Session and python to process conversations and store them in a non-relational database using MongoDB
- The MongoDB schema will support annotating the CRUD functions including classifying, rating, editing and, removing conversations
- A form interface will allow for a data analyst to annotate the conversations
- Real-time chat functionality will be implemented using Flask session and be replace by Flask.socketIO as a future enhancement
- A minimally viable UX is intentional and will be developed using Materialize with Flask frame to focus the initial version of the application on data
- Chat Application will include feature description with instructions, self-service, user account creation, user role and access administration
- MongoDB database schema is API ready for JASON extract for external AI modeling

## Contents

- [Chat with Conversation Annotator](#Chat-with-Conversation-Annotator-for-Chatbot)
- [UX](<##User-Experience-(UX)>)
  - [User Stories](##-User-Stories)
- [Database Model - Chat Annotator](#Database-Model---Chat-Annotator)
  - [Flexible Schema- Collections](##Flexible-Schema---Collections)
  - [Embedded Data Document Structure](##Embedded-Data-Document-Structure)
  - [Single Document](##Single-Document)
  - [Collections Reference Relationships](###-Collections-Reference-Relationships)
- [Development Planes](#-Development-Planes)
  - [Strategy Plane---User Needs and Business Objective](##Strategy-Plane---User-Needs-and-Business-Objective)
- [Scope Plane](##-Scope-Plane)
  - [Personas](###Personas)
  - [Release 1(Current) Features with Database CRUD](<###Release-1(Current)-Features-with-Databse-CRUD>)
  - [Extended Features for future releases](###Extended-Features-for-future-releases)
- [Structure Plane](##Structure-Plane)
  - [MVC Architecture](###MVC-Architecture)
  - [Access to Functions and Navigation by Role Type](###Access-to-Functions-and-Navigation-by-Role-Type)
  - [Navigation Routes Map to Business Function](###Navigation-Routes-Map-to-Business-Function)
- [Skeleton Plane](##Skeleton-Plane)
  - [Wireframes](###Wireframes)
  - [Mobile](####Mobile) - [Computers and Tablets Pages](####Computers-and-Tablets-Pages) -[##Surface Plane](##Surface-Plane)
  - [Defensive Design](###Defensive-Design)
  - [Notification Flash Messages](####Notification-Flash-Messages)
  - [Input Validation](####Input-Validation)
  - [Secure Routes](####Secure-Routes)
  - [Secure Function Access](####Secure-Function-Access)
  - [Error Handling](####Error-Handling)
  - [Code Refactoring](##Code-Refactoring)
- [Testing](##Testing)
- [Heroku Deployment](##Heroku-Deployment)
- [Technologies](##Technologies)
- [Content](###Content)
- [Media](###Media)
- [Tutorial References](##Tutorial-References)
- [References](##References)
- [Credits](##Credits)
- [Acknowledgements](##Acknowledgements)
- [Disclaimer](##Disclaimer)
  <br>

## User Experience (UX)

The purpose is to provide a simple user interface that is intuitive with only the necessary functions for a chat application.

## User Stories

### User Chat Session

1. As a User, I want to be able to select a topic for a conversation to speak with an expert
1. As a User, I want to be able to have a real-time conversation session
1. As a User, I want to be able to review the entire conversation during the session
1. As a User, I want to be notified of a Moderator is online and available for a conversation
1. As a User, I want to be able to end a conversation when completed
1. As a User, I want to be able to handle one active session at any time
1. As a new User, I want to be able to register as a user for the application to participate in a conversation
1. As a retuning User, I want to be to access the application using registered credentials

_Future Enhancment_

- As a returning user, I want to reset my password
- As a User, I want to be able to rate the conversation to provide feedback on whether it was satisfactory
- As a User, I want to be able to provide feedback on the conversation experience

### Moderator Response to User

1. As a Moderator, I want to be able to respond to questions from a user in real-time to assist the user
1. As a Moderator, I want to be able to conduct one active conversation session one at any time
1. As a Moderator, I want to be able to terminate a conversation session to indicate completion of the conversation session
1. As a Moderation, I want to be able to view the list of chats that are pending a moderator to respond
1. As a Moderator, I want to be able to view a list of chats that are currently assigned to other moderators

_Future Enhancment_

1. As a moderator, I want to be able to select to respond to users by topic name

### Chat Conversation Annotator

Review and Rate Conversations

1. As an Annotator, I want to be able to review and annotate conversation to be used for training AI bot
1. As an Annotator, I want to check to see if any new conversations need annotation
1. As an Annotator, I want to be able to search by conversations by topic name for the annotation
1. As an Annotator, I want to be able to rate the quality of the conversation

_Future Enhancement_

1. As an Annotator, I want to be able to reclassify the conversation to the correct topic for training AI Bot
1. As an Annotator, I want to be able to add a new topic to the list of topics
1. As an Annotator, I want to modify the conversation to deliver an accurate response to questions
1. As an Annotator, I want to confirm if user rating aligns with annotation rating

### Chat Administrator Manage Conversation Topic Tags

1. As an Administrator, I want to add new topic tags to categorize conversations
1. As an Administrator, I want to update topic tags to

_Future Enhancements_

- Implement restrictions so that topic tags cannot be deleted when used to tag conversation
- As an Administrator, I can deactivate any user to revoke access to the application
- As an Administrator, I can assign roles to a user
- As an Administrator, I can delete any conversation if requested by the user to comply with GDPR regulation

# Database Model - Chat Annotator

```
Design Principle - Atomicity and Transactions
In most cases, multi-document transaction incurs a greater performance cost over single document writes,and the availability of multi-document transactions should not be a replacement for effective schema design.

For many scenarios, the denormalized data model (embedded documents and arrays) will continue to be optimal for your data and use cases.

That is, for many scenarios, modeling your data appropriately will minimize the need for multi-document transactions.
```

Source: [Atomicity and Transactions](https://docs.mongodb.com/manual/core/write-operations-atomicity/)

## Flexible Schema - Collections

| Collection    | Description                                                                  | Usage                                                                                                                |
| ------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Feature       | Operational Feature Name, Description, and Feature Specific User Instruction | Seeded information used on the feature page stored in the database to allow manual updates without code modification |
| Conversations | Chat conversations between the user and moderator                            | Conversation information and generated messages are stored using the Embedded sub-document structure                 |
| Topics        | Category tag for a conversation                                              | User selects the topic to classify a conversation at initiation                                                      |
| Ratings       | Rate the Quality of conversation                                             | Annotator review and rate the quality of the conversation for training chat-bots                                     |
| Users         | Chat application user role type                                              | Access to application functions are granted based on the user's assigned role type                                   |

---

<br />

## Embedded Data Document Structure

### Conversations

```
{conversations:{
    _id:,
    topic_name:
    username:
    timestamp:
    moderator:
    status:
    msg:[
       {
         timestamp:
         username:
         msgtxt:
       },
       {....
       },
       ....
    ]
```

### Conversation Embedded Sub-document for messages

<br />

| Collection Sub-document | Data Stucture | Elements                                  |
| ----------------------- | ------------- | ----------------------------------------- |
| conversations.msg       | array.object  | ("timestamp", "username", "message text") |

---

<br />

### Features

```
features:{
  _id:
  feature_name:
  feature_description:
  feature_instructions:
}
```

### Features Embedded Sub-document for instructions

<br />

| Feature              | Sub-Document | Elements |
| -------------------- | ------------ | -------- |
| feature_instructions | array.object | [#]      |

---

<br />

## Single Document

### Users

```
users:{
    _id:,
    password: encrypted
    roletype:
}
```

### Topics

```
topics:{
  _id:,
  topic_name
}
```

### Ratings

```
ratings:{
  _id:,
  rating_name
}
```

### Collections Reference Relationships

<br />

| Collection Name.Collection Element | Reference Collection.Element |
| ---------------------------------- | ---------------------------- |
| conversations.topic_name           | topics.topic_name            |
| conversations.username             | users.username               |
| conversations.moderator            | users.username               |
| conversations.rating               | rating.rating_name           |
| conversations.msg.username         | users.username               |

---

<br />

### Collection Element - List of Values

<br />

```
Note: Collections storing the Element list of values are created and seeded manually utilizing CRUD Operations via MongoDB Atlas Data Explorer without any code changes

Future Enhancement: Develop CI/CD CLI scripts to seed and modify the data
```

### Conversation Status Indicator

| Conversation Status | Usage                                                                        |
| ------------------- | ---------------------------------------------------------------------------- |
| pending             | User selected topic and initiated conversation queued for moderator response |
| active              | Moderator responded conversation is active                                   |
| done                | Conversation completed pending annotation                                    |
| annotated           | Annotator reviewed and rated conversation                                    |

---

<br />

#### Rating

| Rating Name | Rating Values                         |
| ----------- | ------------------------------------- |
| Rating      | ("Excellent", "Satisfactory", "Poor") |

---

<br />

#### User Role Type

| Role Type | Role Description                                    |
| --------- | --------------------------------------------------- |
| user      | User is the initiator of conversations              |
| moderator | Response to user initiated conversations            |
| annotator | Reviews completed conversations and assigns ranking |
| admin     | Manages conversation topics                         |

---

<br />

#### Topics

| Topic (Initial Values) | Description                |
| ---------------------- | -------------------------- |
| Create Workspace       | Gitpod workspace           |
| Invoke Terminal        | Gitpod Teminal Session     |
| Git                    | Git commands               |
| Open Workspace         | Gidpod Workspace           |
| Javascript             | Javascript language        |
| Jinja2                 | Jinja templating lanagiage |
| Wireframe              | UX wireframing             |

---

<br />
<details>
<summary>
References: Data Model
</summary>
<p>

- [Data Model Design](https://docs.mongodb.com/manual/core/data-model-design/#std-label-data-modeling-referencing)
- [Perfrom CRUD Operations in Atlas](https://docs.atlas.mongodb.com/data-explorer/)
- [Manage Documents in Data Explorer](https://docs.atlas.mongodb.com/data-explorer/documents/)
- [Operational Factors and Data Models](https://docs.mongodb.com/manual/core/data-model-operations/)

</details>
<br />
# Development Planes

## Strategy Plane - User Needs and Business Objective

The primary goal of the application is to capture and annotate actual conversations for training AI conversational models for chatbots. The conversation domain is specific to an organization that utilizes chatbots to assist with providing support and responses to questions from the user community.

The user will be able to get information for a specific product or service. The business will be able to provide accurate and relevant information to the customer with a high rating.

Generic AI models for chatbot conversations do not capture the specific context of a business and the profile of target customers. There will contribute toward the development of explainable AI models.

Usable data to train AI models for specific contexts that are specific to a domain and fine-tune to a specific business use case is likely to yield the best results.

The focus of the project is on data and inspiration was from [Python Chat Bot Tutorial - Chatbot with Deep Learning (Part 1)](https://www.youtube.com/watch?v=wypVcNIH6D4https://www.youtube.com/watch?v=wypVcNIH6D4). The UX will be developed using Materialize adapted from the design decisions of the Mini Project - Putting It All Together.

## Scope Plane

### Personas

- Chat User initiates conversations
- Chat Moderator respond to conversations
- Chat Conversation Annotator review and rates conversations
- Chat Application Admin manages conversation topics

### Release 1(Current) Features with Databse CRUD

- Chat applications using Flask session and routing to support private conversations between a user and a moderator
- Capture conversations categorized by topic utilizing MongoDB Embedded Data Document Structure
- Data annotation functionality to review and rank the quality of conversation
- Access to application functionality will be base on user role type, specifically, user, moderator, annotator, and application administrator
- The UX will be developed using Materialize adapted from the design decisions of the Mini Project - Putting It All Together

### Extended Features for future releases

- Replace Flask session with [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) to improve reliability, responsiveness, and security
- Data extraction JASON API for training AI Machine Learning models
- CI/CD configuration scripts to replace MongoDB Data Explorer install manually seeded administrator and superuser accounts and lists of values

## Structure Plane

The project utilizes the Flask framework based on the Model-View-Controller (MVC) architecture

### MVC Architecture

![MVC Architecture](static/images/MVCArchitecture.png)
Source: [How Model-View-Controller Architecture Works](https://www.freecodecamp.org/news/model-view-architecture/)
<br />

### Access to Functions and Navigation by Role Type

<br />

| Role      | Features | Register | Login | Logout |
| --------- | -------- | -------- | ----- | ------ |
| All roles | Yes      | Yes      | Yes   | Yes    |

---

<br />

| Role      | Active Chat | Room | Chat List | Manage Topic | Annotate Chat |
| --------- | ----------- | ---- | --------- | ------------ | ------------- |
| User      | Yes         | Yes  | No        | No           | No            |
| Moderator | Yes         | No   | Yes       | No           | No            |
| Annotator | No          | No   | No        | No           | Yes           |
| Admin     | No          | No   | No        | Yes          | No            |

---

<br />

### Navigation Routes Routes Map to Business Function

<br />

The concept of routes and attempt at the art of routing has been a challenge and there is still much to learn to understand routing.

```
Build smart routes to accommodate dynamic applications and APIs

Routes refer to URL patterns e.g. myapp.com/home or myapp.com/about
Views refer to content to be served at these URLs

@app.route("/") Python decorator that assigns URLs to functions

Python decorators are essentially logic which wraps other function and always match the syntax of the link above the function

Name of the view functions hold significance in Flask
```

Tip: We can handle multiple routes with a single function by simply stacking additional route decorators above any route!

```
@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
return "Hello World!"
```

```
Mapping URLs to actions
Reserve URL path associate with a page template (with business logic)

Apps are a medium for data such as user profiles/post

Routes define the ways of access data which is always changing
```

Source: [The Art of Routing in Flask](https://hackersandslackers.com/flask-routes/)

| Business Function     | Routes                                                                                                                                                                                                                   | Decorator                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Features              | @app.route("/") </br> @app.route("/features") </br> @app.route("/get_features")                                                                                                                                          |
| Register              | @app.route("/register", methods=["GET", "POST"])                                                                                                                                                                         | def features(): </br> def get_features():                                                                           |
| Login                 | @app.route("/login", methods=["GET", "POST"])                                                                                                                                                                            | def login():                                                                                                        |
| Logout                | @app.route("/logout")                                                                                                                                                                                                    | def register():                                                                                                     |
| Profile               | @app.route("/profile", methods=["GET"])                                                                                                                                                                                  | def profile():                                                                                                      |
| Topic                 | @app.route("/topic") </br> @app.route("/get_topics")</br> @app.route("/add_topic", methods=["GET", "POST"])</br>@app.route("/edit_topic/<topic_id>", methods=["GET", "POST"])</br>@app.route("/delete_topic/<topic_id>") | def topic(): </br> def get_topics(): </br>def add_topic():</br>edit_topic(topic_id):<br>def delete_topic(topic_id): |
| Chatroom              | @app.route("/chatroom", defaults={"activeconv": ""}, methods=["GET", "POST"])</br>@app.route("/chatroom/<activeconv>", methods=["GET", "POST"])                                                                          | def chatroom(activeconv):                                                                                           |
| Chatlist              | @app.route("/chatlist", defaults={"activeconv": ""}, methods=["GET", "POST"])</br>@app.route("/chatlist/<activeconv>", methods=["GET", "POST"])                                                                          | def chatlist(activeconv):                                                                                           |
| Chat                  | @app.route("/chat", defaults={"activeconv": ""}, methods=["GET", "POST"])</br>@app.route("/chat/<activeconv>", methods=["GET", "POST"])                                                                                  | def chat(activeconv):                                                                                               |
| Annotate Chats        | @app.route("/annotatechats", defaults={"convid": ""}, methods=["GET", "POST"]) </br>@app.route("/annotatechats/<convid>", methods=["GET", "POST"])                                                                       | def annotatechats(convid):                                                                                          |
| Search by Topic       | @app.route("/search", methods=["GET", "POST"])                                                                                                                                                                           | def search():                                                                                                       |
| Delete Topic          | @app.route("/delchat/<delconvid>")                                                                                                                                                                                       | def delchat(delconvid):                                                                                             |
| Custom Error Handling | @app.errorhandler(404)<br>@app.errorhandler(500)<br>@app.errorhandler(405)                                                                                                                                               | def page_not_found(error):</br>def internal_server(error):</br>def method_not_allowed(error):                       |

---

</br>

## Skeleton Plane

### Wireframes

#### Mobile

<details>
<summary>
Mobile
</summary>
<p>
 
##### Welcome Page - [View](https://github.com/)

![Mobile  Chat Welcome Page](static/images/ChatUIWelcome.gif)

##### Mobile Chat Dashboard

![Mobile Chat Dashboard](static/images/mobileChatDashboard.png)

##### Mobile Chat Widget

![Mobile Chat Panel](static/images/mobileChatPanel.png)

##### Mobile Rating Conversation

![Rating](static/images/rating.png)

##### Mobile Chat Admin

![Admin Panel](static/images/adminPanel.png)

##### Mobile Annotate Conversations

![Annotate Conversation](static/images/annotateConversations.png)

##### Mobile Application Administration

![pythonGrid](static/images/pythonGrid.png)
Source: [PythonGrid](https://pythongrid.com/)

#### Error Message Pages

##### 404 Not Found Page

![404 Page](static/images/404Page.png)

Source: [Python Flask Tutorial: Full-Featured Web App Part 12 - Custom Error Pages](https://www.youtube.com/watch?v=uVNfQDohYNI)

[Flask Custom Error pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)

##### 403 Do Not Have Permission

![403 Page](static/images/404Page.png)

##### 500 Internal Server

![500 Page](static/images/500Page.png)

</details>
<br />

#### Computers and Tablets Pages

<details>
<summary>
Computer and Large Devices
</summary>
<p>

##### Chat Welcome Page

![Mobile Chat Welcome Page](static/images/chatWelcome.png)

##### Chat Dashboard

![Chat Dashboard](static/images/chatDashboard.png)

##### Chat Panel

![Chat Panel](static/images/chatPanel.png)

##### Data Processing and Annotate Conversations

![pythonGrid](static/images/pythonGrid.png)

Source: [PythonGRid](https://pythongrid.com/)

##### Application Administration

![pythonGrid](static/images/pythonGrid.png)

Source: [PythonGRid](https://pythongrid.com/)

##### Topic Category Values

- Category
- Rating

![Rating](static/images/rating.png)

#### Support pages

##### 404 Not Found Page

![404 Page](static/images/404Page.png)

##### Contact Us Page Wireframe

![Contact Us](static/images/contactUs.png)

Source:
[25 Best Contact Us Page Examples to Inspire Yours (Updated for 2020)](https://www.impactplus.com/blog/best-contact-us-page-examples)

</details>
<br />

## Surface Plane

### Defensive Design

#### Notification Flash Messages

#### Secure Routes

#### Secure Function Access

#### Input Validation

all input data is validated (e.g. presence check, format check, range check)

- Edit_topic decorator fucntion does not handle invalid ObjectId

Issue: Invalid ObjectId renders bson-errors.invalidid
Resolution:
bson.objectid.ObjectId.is_valid('54f0e5aa313f5d824680d6c9')
=> True
bson.objectid.ObjectId.is_valid('54f0e5aa313f5d824680d')
=> False

![Not a valid ObjectID](static/images/notValidObjectId.png)

Source: [How to check that mongo ObjectID is valid in python?](https://stackoverflow.com/questions/28774526/how-to-check-that-mongo-objectid-is-valid-in-python)

#### Error Handling

internal errors are handled gracefully and users are notified of the problem where appropriate.

## Code Refactoring

#### Use len() function instead of For Loop

```
initconvId = conversations[len(conversations)-1]['_id']
```

```
for conversation in conversations:
        initconvId = conversation['_id']
```

Source: [Python len() Function](<https://www.w3schools.com/python/ref_func_len.asp#:~:text=The%20len()%20function%20returns,of%20characters%20in%20the%20string>)

## Heroku Deployment

```
HIGH-LEVEL STEPS:
1. Create a Heroku App
2. Connect Git remote
3. Add requirements.txt
4. Add Procfile

Note: Includes Forking Github Repository
```

<details>
<summary>
Heroku Deployment
</summary>
<p>

#### Create a Heroku Account

- Navigate to Heroku.com
- Click on "Sign Up" and create a new account
- Fill out the form provide a first name, last name ,and email address
- Select Python as the Primary Development Language
- Confirm that you are not a Robot
- Click "Create Free Account"
- Heroku will send you a confirmation email
- Copy the link provided in the email and paste it into a new tab
- You will be prompted to set a password
- You may skip selecting if you like to receive occasional updates
- Click "Set Password and Log in"

#### Heroku Dashboard

- Click on Python as the language
- The Heroku Dev center will be rendered
- Click on the browser back button
- Click on "Create New App" button
- Name must not be used by anyone else
- Provide App Name (Note name does not allow space so use hyphens)
- Select region closes to you
- Click on "Create App"

#### Heroku Toolbelt - CLI with gitpod terminal

- Go to your Gitpod project terminal
- Install
  ```
  npm install -g heroku
  ```
- login to Heroku using your account details
  ```
  heroku login -i
  ```
- List heroku apps
  ```
  Apps
  ```
- Rename app and reference it
  (NoteL replace <app name> with the app name)
  ```
  heroku apps:rename <app name> --app <app name>
  ```
- Confirm that your app was successfully renamed
  ```
  Apps
  ```

#### Open App Heroku Dashboard

- Click on "Open App"
- Note the URL for the app is
  ```
  https://APP-NAME.herokuapp.com
  ```

#### Pushing code to Heroku from CLI

- Add a requirements.txt file
  Contains python dependencies

  ```
  pip3 freeze --local > requirements.txt
  git add -a requirements.txt
  git commit -m "Add requirements.txt"
  git push -u heroku main
  ```

- Add a Procfile
  Tells Heroku how to run a project

```
  echo web: python app.py > Procfile
  git add - Procfile
  git commit -m "Add Procfile"
  git push -u heroku main
```

#### Add Heroku Config Vars

- Naviagte to Heroku dashboard
- Click on Settings
  Note: SECRET KEY and KEY string without the quotes in found in env.py file

  ```
  IP 0.0.0.0
  PORT 5000
  SECRET_KEY <copy from env.py>
  KEY <copy from env.py>
  MONGO_URI <copy from env.py>
  MONGO_DBNAME <chat_annotate>
  ```

- Click on "More" and "View Logs"
- Alternatively, select "Restart all Dynos" to restart the app

#### Link GitHub Repository to Heroku for automatic deployment from HitHub

- Navigate to Heroku
- Click on Deploy tab
- Deployment Method Click Github
- Paste github repository name and click "Search"(the github repo name from github)
- Click on "Connect"
- Click "Enable Automatic Deploys" from the master branch
- Click "Deploy Branch"

#### Push Code from Gitpod

- in Gitpod navigate to project folder
  ```
  git remote -v
  git status
  git remote rm heroku
  git remote -v
  git status
  git add - A
  git commit -m "Push to GitHub"
  git push origin master
  ```
- Go to github repo and check that the recent push worked

### Validate Deploymnent on Heroku

- Navigate to Heroku
- Click on "Deploy Branch
- Click on "Activity" Tab and "View Build Log"
- Open the app to check that it opens

## Forking the GitHub Repository

By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps...

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. You should now have a copy of the original repository in your GitHub account.

### Making a Local Clone

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. Under the repository name, click "Clone or download".
3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

7. Press Enter. Your local clone will be created.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `CI-Clone`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Click [Here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository#cloning-a-repository-to-github-desktop) to retrieve pictures for some of the buttons and more detailed explanations of the above process.

</details>
<br />

## Testing

[Testing Documentation here.](TESTING.md)

## Technologies

### Web Development

- Materialize
- Flask
- MongoDB
- Python
- Javascript
- HTML5
- CSS
- Font Awesome

### Deployment, Source Code Repository, Version Control and Project Management

- Heroku
- GitHub
- GitHub Projects

### Development Tools

- Chrome DEV Tool
- Firefix Developer Edition
- Gitpod
- Visual Studio Code (VSCode)
- Balsamiq
- SnagIt
- [Markdown TOC](https://ecotrust-canada.github.io/markdown-toc/)
- Microsoft Edge

### Validators

- [CSS Beautifier](https://www.freeformatter.com/css-beautifier.html)
- [WCAG Color contrast checker](https://chrome.google.com/webstore/detail/wcag-color-contrast-check/plnahcmalebffmaghcpcmpaciebdhgdf?hl=en)
- [Responsive Design Checker](http://ami.responsivedesign.is/)
- Chrome Dev Tool
  - JS loaded using dev tool/network
- [Jshint](https://jshint.com/)

### Accessibility Audit

- Chrome Dev Tool
  - Ligthouse Accessibility

## Content

- UX adopted and modified from CI Mini Project- Putting it all together
- All content and data were created by the developer

## Media

- [Dreamstime chatbot icon](https://thumbs.dreamstime.com/b/chatbot-icon-virtual-assistant-vector-143083940.jpg)
- All images were created by the developer

## Tutorial References

<br />
<details>
<summary>
Tutorials
</summary>
<p>

- [Build a Simple CRUD App with Python, Flask, and React](https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react)
- [Node.js: Real-Time Web with Socket.IO](https://www.lynda.com/Node-js-tutorials/Course-prerequisites/633868/685558-4.html?srchtrk=index%3a14%0alinktypeid%3a2%0aq%3aflask_socketio%0apage%3a1%0as%3arelevance%0asa%3atrue%0aproducttypeid%3a2)
- [Building your first Chat Application using Flask in 7 minutes](https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d)
- [Simple boilerplate for ChatterBot using Flask](https://xscode.com/chamkank/flask-chatterbot)
- [Python Chat Bot Tutorial - Chatbot with Deep Learning (Part 1)](https://www.youtube.com/watch?v=wypVcNIH6D4https://www.youtube.com/watch?v=wypVcNIH6D4)
- [Livechat Bot Transfer users from a bot to a live agent](https://www.appypie.com/chatbot/livechat-bot)
- [Creating a Discord Bot from Scratch and Connecting to MongoDB](https://towardsdatascience.com/creating-a-discord-bot-from-scratch-and-connecting-to-mongodb-828ad1c7c22e)
- [How To Make A Chatbot In Python?](https://www.edureka.co/blog/how-to-make-a-chatbot-in-python/)
- [1.1: fetch() - Working With Data & APIs in JavaScript](https://www.youtube.com/watch?v=tc8DU14qX6I&feature=youtu.be)
- [How to use Fetch with JavaScript](https://www.youtube.com/watch?v=tVQgfKqbX3M&feature=youtu.be)
- [JavaScript this Keyword Explained In 3 Minutes](https://www.youtube.com/watch?v=Pi3QC_fVaD0)
- [JavaScript Promise in 100 Seconds](https://www.youtube.com/watch?v=RvYYCGs45L4)
- [Intro To JavaScript Unit Testing & BDD (2 Hour+ Course)](https://www.youtube.com/watch?v=u5cLK1UrFyQ&feature=youtu.be)
- [Awesome Python Awesome A curated list of awesome Python frameworks, libraries, software and resources.](https://awesome-python.com/)

</details>
<br />

## References

<br />

<details>
<summary>
References
</summary>
<p>

- [ChatterBot](https://chatterbot.readthedocs.io/en/stable/)

- [The MongoDB 4.2 Manual](https://docs.mongodb.com/v4.2/)

- [Let’s Build an Intelligent Chatbot](https://www.kdnuggets.com/2019/12/build-intelligent-chatbot.html)

#### Database schema

- [Data Model Design](https://docs.mongodb.com/manual/core/data-model-design/)
- [Operational Factors and Data Models](https://docs.mongodb.com/manual/core/data-model-operations/)
- [Model Data for Atomic Operations Pattern](https://docs.mongodb.com/manual/tutorial/model-data-for-atomic-operations/#data-modeling-atomic-operation)
- [MongoEngine](http://docs.mongoengine.org/tutorial.html)

#### MONGODB CRUD

- [Transactions and Operations](https://docs.mongodb.com/manual/core/transactions-operations/#transactions-operations-crud)
- [Query an Array](https://docs.mongodb.com/manual/tutorial/query-arrays/#read-operations-arrays)
- [Query on Embedded/Nested Documents](https://docs.mongodb.com/manual/tutorial/query-embedded-documents/#read-operations-embedded-documents)
- [Model Data to Support Keyword Search](https://docs.mongodb.com/manual/tutorial/model-data-for-keyword-search/)

#### SocketIO

- [Polling vs WebSockets vs Socket.IO (Simple Explanation) - Chat App Part11](https://www.youtube.com/watch?v=sUEq35F-ELY)
- [Create Chat Applicaton Using Flask-SocketIO - Chat App Part12](https://www.youtube.com/watch?v=zQDzNNt6xd4)
- [Node.js:Real-Time Web Socket.IO](https://www.lynda.com/Node-js-tutorials/Node-js-Real-Time-Web-Socket-IO/633868-2.html)

#### Flask-Login

- [Flask-login](https://flask-login.readthedocs.io/en/latest/)

#### Flask-Session

- [Flask-Session](https://flask-session.readthedocs.io/en/latest/#version-0-4)

#### Documentation

- [Demo your App in your GitHub README with an Animated GIF](https://dev.to/kelli/demo-your-app-in-your-github-readme-with-an-animated-gif-2o3c)

- [How to use JSDoc - Basics & Introduction](https://www.youtube.com/watch?v=Nqv6UkTROak)
- [Code Institue Sample ReadMe](https://github.com/Code-Institute-Solutions/SampleREADME)

#### UX

- [Chatbot Design](https://dribbble.com/tags/chatbot?page=19&s=latest)
- [8 beautiful chatbot UI examples that will definitely inspire you](https://www.digital22.com/insights/beautiful-chatbot-ui-examples-that-will-definitely-inspire-you#a6)

##### UX Sources Credits

- [Chat UI Welcome Screen from Vlad Tyzum](https://www.digital22.com/insights/beautiful-chatbot-ui-examples-that-will-definitely-inspire-you#a6)
- [Dashboard and Chat](https://dribbble.com/shots/10978875-Insurance-app-dashboard-Chat)
- [Direct Messaging](https://dribbble.com/shots/10831579-013-Direct-Messaging-UI-Challenge)

##### Alternate UX Sources

- [Chatbot](https://dribbble.com/shots/10997646-Chatbot-for-US-police-departments)
- [Create Chat Bots](https://dribbble.com/shots/10810904-Chat-Bots)
- [Corporate Chat Widget](https://dribbble.com/shots/10770064-Corporate-chat-widget)

</details>
<br />

## Acknowledgements

- My Mentor Guido Cecilio for his feedback and guidance
- Tutor Tim Nelson over and beyond for guidance and technical support and encouragement to take on the daunting code challenges
- Fellow learner Mihaela Sandrea who took the time to provide user acceptance feedback and testing
- Slack community members who provided support to survive the learning journey

## Disclaimer

This project is for educational use only
