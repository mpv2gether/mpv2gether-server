from random import choice
from constants import message_types, error_types
from helpers.parse_helper import get_key, MissingKeyError

sessions = {}
users = {}

async def create(ws, message):
    if ws in users:
        await message_types.Error(error_type=error_types.in_another_session, error="You're in another session, consider leaving it first: {}".format(users[ws].session.key)).send(ws)
        return
    try:
        nick = get_key(message, "nick")
    except MissingKeyError as e:
        await message_types.Error(error_type=error_types.missing_key, error=str(e)).send(ws)
        return
    session_key = await generate_key()
    user = MPV2GetherUser(nick, ws)
    session = MPV2GetherSession(user, session_key)
    user.set_session(session)
    sessions[session_key] = session
    users[ws] = user
    await message_types.CreatedSession(sender=ws, session_key=session_key).send(ws)

async def join(ws, message):
    if ws in users:
        await message_types.Error(error_type=error_types.in_another_session, error="You're in another session, consider leaving it first: {}".format(users[ws].session.key)).send(ws)
        return
    try:
        session_key = get_key(message, "session_key")
        nick = get_key(message, "nick")
    except MissingKeyError as e:
        await message_types.Error(error_type=error_types.missing_key, error=str(e)).send(ws)
        return
    if session_key not in sessions:
        await message_types.Error(error_type=error_types.invalid_key, error="Not a session_key: {}".format(session_key)).send(ws)
        return
    session = sessions[session_key]
    if any([x.nick == nick for x in session.users]):
        await message_types.Error(error_type=error_types.nick_taken, error="This nick is already taken: {}".format(nick)).send(ws)
        return
    user = MPV2GetherUser(nick, ws)
    session.add_user(user)
    user.set_session(session)
    users[ws] = user
    for x in session.users:
        await message_types.UserJoined(sender=ws).send(x.ws)

async def leave(ws, message):
    if not ws in users:
        await message_types.Error(error_type=error_types.not_in_session, error="You're not in a session, so you can't leave.").send(ws)
        return
    session = users[ws].session
    for x in session.users:
        await message_types.UserLeft(sender=ws).send(x.ws)
    session.remove_user(ws)
    users.pop(ws)

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
