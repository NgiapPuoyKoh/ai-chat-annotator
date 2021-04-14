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

- Replace Flask session with Flask SocketIO to improve reliability, responsiveness, and security
- Data extraction JASON API for training AI Machine Learning models
- CI/CD configuration scripts to replace MongoDB Data Explorer install manually seeded administrator and superuser accounts and lists of values

# Database Model - Chat Annotator

```
Design Principle - Atomicity and Transactions

In most cases, multi-document transaction incurs a greater performance cost over single document writes,and the availability of multi-document transactions should not be a replacement for effective schema design.

For many scenarios, the denormalized data model (embedded documents and arrays) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for multi-document transactions.

Source:[Atomicity and Transactions](https://docs.mongodb.com/manual/core/write-operations-atomicity/)

```

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
## Contents

- [Chat with Converation Annotator](#Chat-with-Conversation-Annotator-for-Chatbot)
  - [UX](#ux)
    - [User Stories](#user-stories)
  - [Development Planes](#development-planes)
    - [Strategy Plane - User Needs and Business Objective](#strategy-plane---user-needs-and-business-objective)
    - [Identify Business Goals and Objectives](#identify-business-goals-and-objectives)
    - [Scope Plane](#scope-plane)
      - [User Stories (Future)](#user-stories--future-)
    - [Structure Plane](#structure-plane)
    - [Skeleton Plane](#skeleton-plane)
      - [Existing Features](#existing-features)
      - [Features Left to Implement](#features-left-to-implement)
    - [Future feature idea](#future-feature-idea)
    - [Surface Plane - Visual Design](#surface-plane---visual-design)
    - [Database Model - Chat Annotator](#Database-schema-chat-annotator)
  - [Technologies Used](#technologies-used)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [References](#references)
  - [Content](#content)
  - [Credits](#credits)
  - [Acknowledgements](#acknowledgements)
  - [Disclaimer](#disclaimer)

## References

### DataModel

- [Data Model Design](https://docs.mongodb.com/manual/core/data-model-design/#std-label-data-modeling-referencing)
- [Perfrom CRUD Operations in Atlas](https://docs.atlas.mongodb.com/data-explorer/)
- [Manage Documents in Data Explorer](https://docs.atlas.mongodb.com/data-explorer/documents/)
- [Operational Factors and Data Models](https://docs.mongodb.com/manual/core/data-model-operations/)

# Development Planes

# Chat Process and CRUD Functionality
