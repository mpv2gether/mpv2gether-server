import handlers.session_handler as session_handler
import json, websockets

# all message types
message_types = {
    #server
    "error",
    "created_session",
    "user_joined",
    "user_left",
    #client
    "create_session",
    "join_session",
    "leave_session",
    #both
    "message"
}

# classes for server-side messages
class Message():
    def __init__(self, type, **args):
        self.type = type
        vars(self).update(args)
    async def send(self, ws):
        message = vars(self).copy()
        message.pop("type")
        r_json = json.dumps({"type":self.type, "message":message})
        try:
            await ws.send(r_json)
        except websockets.exceptions.ConnectionClosed:
            await session_handler.leave(ws)

class TMessage(Message):
    def __init__(self, message, sender):
        Message.__init__(self, "message", nick=session_handler.users[sender].nick, message=message)

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
        Message.__init__(self, "created_session", nick=session_handler.users[sender].nick, session_key=session_key)

# variables for client-size ones
create_session    = "create_session"
join_session      = "join_session"
leave_session     = "leave_session"
message           = "message"