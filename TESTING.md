## End to End Testing

**Important Testing Notes**

- To test the chat functionality it will be necessary to use different browsers and/or different devices when logged in as a persona (Chrome/Firefox/Edge). The reason is that it utilizes flask session
- Avoid clearing browser cache so that sessions remain active for returning users. Clearing browser cache may be necessary to start over active chat sessions
- Registration of user account is only for role type user.
- To create accounts as moderator, admin, and annotator register as you would as a user. Provide me with the username and the role type and I will have to update it directly using MongoDB data explorer

## General Scenario

- Conversations are one moderator to one user
- Each User and Moderator can only engage in one active conversation at any time.
- The conversations are initiated by the user and once a session is ended it cannot be continued
- The user or moderator will be able to continue conversations if the browser session is not deleted.
- A moderator login and can review and respond to chats that are pending a response
- User can engage in a real-time conversation with the moderator
- Annotator will review and rate completed conversations

## End to End Chat Session Test Matrix

| Test Case                    | User Story                                                                                | Feature                                                                             | Expected Result                                                                              | Actual Result                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Chat Features                | As a user, I want to know how to start using the application                              | Feature Page                                                                        | Direct user to quick start link by role type                                                 | Card panels provide quick- start info and when clicked provides more details on what each feature does        |
| Initiate Conversation        | As a user, I want to select a topic and initiate a conversation                           | Click on Room Link                                                                  | Renders Page for user to select topic and click start chat                                   | User is redirected to Active chat page with a flash message that conversation is pending Moderator's response |
| Send message                 | As a user, I want to be able to send a message during an active conversation              | Message text area and send button captures message entered by user                  | The message entered by the user will appear in the display text area with a timestamp        | Page refresh and displays all messages entered by the user or moderator of the conversation                   |
| End Conversation             | As a user, I want to end the conversation                                                 | Use clicks on the end button                                                        | User will be redirected to Chat Room. Flash message render to confirm conversation has ended | User is redirected to chat room                                                                               |
| User sees moderator response | As a user, I want to be able to see moderator responses as they are entered in real-timee | Messages entered by the moderator will be displayed in the active chat message area | Messages are displayed when entered in real-time                                             | Page refresh with messages deisplayed when no keys are pressed                                                |

---

## Functional User Stories Role Type Test Matrix

| Test Case | User Story                                                                         | Feature          | Expected Result         | Actual Result                                         |
| --------- | ---------------------------------------------------------------------------------- | ---------------- | ----------------------- | ----------------------------------------------------- |
| 1         | As a user, I want to register a user account                                       | Register Account | Successful registration | Directed to User with access to user navbar functions |
| 2         | As a user, I can logout                                                            | Logout and Login | Successful logout       | Directed to login page                                |
| 3         | As a returning user, I can login using credentials used to register a user account | Successful Login | Directed to Chat Page   |

---

# Unit Testing

## Unable to trigger a POST to perform an update

Issue: Unable to perform an update to set the status of a conversation record using a select and button

```
An invalid form control with name='rating_name' is not focusable.
```

Resolution:
Remove the required attribute from the select for rating list

```
<select id="rating_name" name="rating_name" class="validate" required>

<select id="rating_name" name="rating_name" class="validate" >
```

## Collapsible Accordian

Records are displayed using a materialize collapsible accordion each with a select list and button. The id of the first record is being picked up instead of the record selected for updated

Issue: The first conversation displayed is being updated instead of the one selected by the user

Resolution:
Placement of the form end tag needs to be inside within the jinja for loop

Source: [How To Fix: An invalid form control with name=’x’ is not focusable error](https://www.geekinsta.com/how-to-fix-an-invalid-form-control-with-name-is-not-focusable/)

## MongoDB find_one_and_update syntax to combine $set and $push

Issue: Unable to combine into one

```
            # insert final message of conversation
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$push": {"msg": {"timestamp": msgtime,
                                   "username": session["user"],
                                   "msgtxt": request.form.get("msgtxt")}}})

            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$set": {"status": "done"}})
```

Error:

```
pymongo.errors.OperationFailure
pymongo.errors.OperationFailure: Unrecognized pipeline stage name: '$push', full error: {'operationTime': Timestamp(1618923014, 1), 'ok': 0.0, 'errmsg': "Unrecognized pipeline stage name: '$push'", 'code': 40324, 'codeName': 'Location40324', '$clusterTime': {'clusterTime': Timestamp(1618923014, 1), 'signature': {'hash': b'\x06\xa4\xae\x81\xbc\xfd\x9c\xb4\\\x13\xaaf\x05:\xaf\xb9\xf9}\x99`', 'keyId': 6917341148591685635}}}
```

Resolved:

```
            # capture message text and set status
            mongo.db.conversations.find_one_and_update(
                {"_id": ObjectId(session["activeconv"])},
                {"$push": {"msg": {"timestamp": msgtime,
                                   "username": session["user"],
                                   "msgtxt": request.form.get("msgtxt")}},
                 "$set": {"status": "done"}})

```

Source: [How do I setandpush in single update with MongoDB?](https://www.tutorialspoint.com/how-do-i-set-and-push-in-single-update-with-mongodb)

## Unsecure chat url to unathorized conversation by moderator and user

Issue: Moderator is able to access active conversation by using the url initiated by user

Fix: Validate if moderator has an active chat session and access to conversation

```
            # if moderator has an active chat session for active conversation
            if ('convstatus' in session) and (
                    session['convstatus'] == "active") and (
                        'activconv' in session):
```

## Chat Interface

### Polling

### Text Area for Message

</br>

# Known Issues

## Most but not all senarios where url are modified to access conversation using objectid

Issue: Knowledge of how to handle Route validation is not sufficient to code for all scenarios.

## A new browser session is required to engage in a conversation

Issue: If a browser back button is pressed it renders previous page is not removed and a different user access the application it will will display page information from the previous session

Future Enhancement:
Implement a solution is to use SocketIO

## Browser back button during chat renders previous page before refreshed by polling

Issue: If a browser back button is pressed on chat page afte entering message it rerenders message that was previously entered

![backbuttonChat](static/images/backbuttonChatIssue.png)

## Topic Search for some words does not render No result found exception

Issue: The word python does not render the message "No Results Found" message

Attempts to fix error:

- Use strip() to remove trailings spaces

```
    query = request.form.get("query")
    conversations = list(mongo.db.conversations.find(
        {"$text": {"$search": query}}))

```

## Moderator accessing Done conversation error in the same session after completing the conversation

Issue: Monderator using url to a conversation that is done renders a KeyError: 'activeconv'
![ModeratorAccessDoneConv](static/images/moderatorAccessDoneConversationError.png)

## Active Conversations Not Accessible if Sessions is not longer available

Issue: If the browser session information is deleted there is currently no function available
to track and enable users to access and continue the converstion

Enhancement for Future Release:
Replace session and polling with Flask-Scoket IO to remove dependency on session

## Polling removes message text if on keydown pressed

Message entered by User if Send is not clicked and there are no keydown events detected within a few seconds it will be lost

Issue: Limitation of Polling with keydown event time limit

Future Enhancement:
Reimplement solution using Flask-SocketIO or alternative asynch methods
