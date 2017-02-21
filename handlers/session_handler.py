import asyncio
from random import choice
from api import send_json
from constants import message_types, error_types

sessions = {}
users = {}

async def create(ws, message):
    if ws in users:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.in_another_session, "error":"You're in another session, consider leaving it first: {}".format(users[ws].session.key)})
        return
    try:
        nick = message["nick"]
    except KeyError:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.missing_key, "error":"Missing key: nick"})
        return
    session_key = await generate_key()
    user = MPV2GetherUser(nick, ws)
    session = MPV2GetherSession(user, session_key)
    user.set_session(session)
    sessions[session_key] = session
    users[ws] = user
    await send_json(target=ws, type=message_types.created_session, data={"nick":nick, "session_key":session_key})

async def join(ws, message):
    if ws in users:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.in_another_session, "error":"You're in another session, consider leaving it first: {}".format(users[ws].session.key)})
        return
    try:
        session_key = message["session_key"]
    except KeyError:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.missing_key, "error":"Missing key: session_key"})
        return
    try:
        nick = message["nick"]
    except KeyError:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.missing_key, "error":"Missing key: nick"})
        return
    if session_key not in sessions:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.invalid_key, "error":"Not a session_key: {}".format(session_key)})
        return
    session = sessions[session_key]
    if True in [x.nick == nick for x in session.users]:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.nick_taken, "error":"This nick is already taken: {}".format(nick)})
        return
    user = MPV2GetherUser(nick, ws)
    session.add_user(user)
    user.set_session(session)
    users[ws] = user
    for x in session.users:
        await send_json(target=x.ws, type=message_types.user_joined, data={"nick":nick})

async def leave(ws, message):
    if not ws in users:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.not_in_session, "error":"You're not in a session, so you can't leave."})
        return
    sessions[users[ws].session.key].remove_user(ws)
    users.pop(ws)
    await send_json(target=ws, type=message_types.left_session, data={})

charpool = "ABCDEFGHIJKLMNOPQRSTUVWJYZabcdefghijklmnopqrstuvwxyz0123456789"
async def generate_key():
    return "".join(choice(charpool) for _ in range(20))

class MPV2GetherSession():
    def __init__(self, creator, key):
        self.creator = creator
        self.key = key
        self.users = [creator]
    def add_user(self, user):
        self.users.append(user)
    def remove_user(self, user):
        self.users.remove(user)

class MPV2GetherUser():
    def __init__(self, nick, ws):
        self.nick = nick
        self.ws = ws
    def set_session(self, session):
        self.session = session