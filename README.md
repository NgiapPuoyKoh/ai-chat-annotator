# <h1 align="center">Chat with Conversation Annotator for Chatbot </h1>

[View the live project here.](http://flask-ai-chat-annotate.herokuapp.com/getfeatures)

This is a chat application interface with a conversation data annotation feature. It is designed to capture actual conversations via the chatbot with annotation to improve the accuracy and quality of the bot conversations.
Data annotators will have access to annotate chat conversations for training AI chatbot for greater accuracy of Chatbot conversations

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

### Moderator

1. As a Moderator, I want to be able to respond to questions from a user in real-time to assist the user
1. As a Moderator, I want to be able to conduct one active conversation session one at any time
1. As a Moderator, I want to be able to terminate a conversation session to indicate completion of the conversation session

_Future Enhancment_

1. As a moderator, I want to be able to select to respond to users by topic name

### Chat Conversation Annotator

Review and Rate Conversations

1. As an Annotator, I want to be able to review and annotate conversation to be used for training AI bot
1. As an Annotator, I want to check to see if any new conversations need annotation
1. As an Annotator, I want to be able to search by conversations by topic name for the annotation
1. As an Annotator, I want to be able to rate the quality of the conversation

_Future Enhancement_

1. As an Annotator, I want to be able to reclassify the conversation to the correct topic for training Ai Bot
1. As an Annotator, I want to be able to add a new topic to the list of topics
1. As an Annotator, I want to modify the conversation to deliver an accurate response to questions
1. As an Annotator, I want to confirm if user rating aligns with annotation rating

### Chat Application Administrator

Manage Topic Tags

1. As an Administrator, I want to add new topic tags to categorize conversations
1. As an Administrator, I want to update topic tags to

_Future Enhancements_

- Implement restrictions so that topic tags cannot be deleted when used to tag conversation
- As an Administrator, I can deactivate any user to revoke access to the application
- As an Administrator, I can assign roles to a user
- As an Administrator, I can delete any conversation if requested by the user to comply with GDPR regulation

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

### Release 1(Current) Features with Database updates

- Chat applications using Flask session and routing to support private conversations between a user and a moderator
- Capture conversations categorized by topic utilizing MongoDB Embedded Data Document Structure
- Data annotation functionality to review and rank the quality of conversation
- Access to application functionality will be base on user role type, specifically, user, moderator, annotator, and application administrator
- The UX will be developed using Materialize adapted from the design decisions of the Mini Project - Putting It All Together

### Extended Features for future releases

- Replace Flask session with [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) to improve reliability, responsiveness, and security
- Data extraction JASON API for training AI Machine Learning models
- CI/CD configuration scripts to replace MongoDB Data Explorer install manually seeded administrator and superuser accounts and lists of values

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

#### Conversation Status Indicator

Usage:

| Conversation Status | Usage                                                                        |
| ------------------- | ---------------------------------------------------------------------------- |
| pending             | User selected topic and initiated conversation queued for moderator response |
| active              | Moderator responded conversation is active                                   |
| done                | Conversation completed pending annotation                                    |  |  | annotated | Annotator reviewed and rated conversation |

---

<br />

#### Rating

| Rating Name | Rating Values                         |
| ----------- | ------------------------------------- |
| Rating      | ("Excellent", "Satisfactory", "Poor") |

---

<br />

#### User Role Type

| User Role Type | Roles                                               |
| -------------- | --------------------------------------------------- |
| user           | User is the initiator of conversations              |  |  | moderator | Respond to user conversations |
| annotator      | Reviews completed conversations and assigns ranking |
| admin          | Manages Topics                                      |

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

## Tutorials

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

## Content

- All content was written by the developer.
- Psychological properties of colors text in the README.md was found [here](http://www.colour-affects.co.uk/psychological-properties-of-colours)

## Media

- [Dreamstime chatbot icon](https://thumbs.dreamstime.com/b/chatbot-icon-virtual-assistant-vector-143083940.jpg)
- All images were created by the developer

## Acknowledgements

- My Mentor Guido Cecilio for his feedback.
- Tutor Tim Nelson over and beyond for guidance and technical support and encouragement to take on the daunting code challenges
- Fellow learner Mihaela Sandrea took the time to provide user acceptance feedback and testing
- Slack community members who provided support to survive the learning journey

## Disclaimer

This project is for educational use only
