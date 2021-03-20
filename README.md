<h1 align="center">Chat with Conversation Annotator for Chatbot</h1>

[View the live project here.](http://flask-ai-chat-annotate.herokuapp.com/getfeatures)

This is a chat application interface with a conversation data annotation feature. It is designed to capture actual conversations via the chatbot with annotation to improve the accuracy and quality of the bot conversations.
Data annotators will have access to annotate chat conversations for training AI chatbot for greater accuracy of Chatbot conversations

<h2 align="center"><img src="https://thumbs.dreamstime.com/b/chatbot-icon-virtual-assistant-vector-143083940.jpg" alt="chatbot Icon" width=200" height="200"></h2>

## Operational Features

A chat application with conversation data prep to feed into an AI model (not included in the scope)

- Build a real-time chat application (chat room if not too complex) for one on one conversations
- Using Flask and python to process conversations and store them in a non-relational database using MongoDB 
- The MongoDB schema will support annotating the CRUD functions including classifying, rating, editing and, removing conversations
- A form interface will allow for a data analyst to annotate the conversations
- Real-time chat functionality will be implemented using Flask session and be replace by Flask.socketIO as a future enhancement
- A minimally viable UX is intentional and will be developed using Materialize with Flask frame to focus the initial version of the application on data
- Chat Application will include feature description with instructions, self-service, user account creation, user role and access administration
- API for JASON extract for external AI modeling use
