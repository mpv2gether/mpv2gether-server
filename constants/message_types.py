import handlers.session_handler as session_handler
import json

class Message():
    def __init__(self, type, **args):
        self.type = type
        vars(self).update(args)
    async def send(self, ws):
        r_json = json.dumps(vars(self))
        await ws.send(r_json)

class TMessage(Message):
    def __init__(self, message, sender):
        Message.__init__(self, "message", message=message, nick=session_handler.users[sender].nick)

class UserJoined(Message):
    def __init__(self, sender):
        Message.__init__(self, "user_joined", nick=session_handler.users[sender].nick)

class UserLeft(Message):
    def __init__(self, sender):
        Message.__init__(self, "user_left", nick=session_handler.users[sender].nick)

class Error(Message):
    def __init__(self, error_type, error):
        Message.__init__(self, "error", error_type=error_type, error=error)

class CreatedSession(Message):
    def __init__(self, session_key, sender):
        Message.__init__(self, "created_session", session_key=session_key, nick=session_handler.users[sender].nick)


message_types = {
    #server
    "error",
    "created_session",
    "user_joined",
    "left_session",
    #client
    "create_session",
    "join_session",
    "leave_session",
    #both
    "message"
}

#server
error = "error"
created_session = "created_session"
user_joined = "user_joined"
left_session = "left_session"
#client
create_session = "create_session"
join_session = "join_session"
leave_session = "leave_session"
#both
message = "message"
