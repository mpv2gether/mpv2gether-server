import handlers.session_handler as session_handler
from api import send_json
from constants import message_types, error_types

async def message(ws, w_message):
    if not ws in session_handler.users:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.not_in_session, "error":"You're not in a session, so you can't send a message."})
        return
    try:
        t_message = w_message["message"]
    except KeyError:
        await send_json(target=ws, type=message_types.error, data={"error_type":error_types.missing_key, "error":"Missing key: message"})
        return
    for x in session_handler.users[ws].session.users:
        await send_json(target=x.ws, type=message_types.message, data={"nick":session_handler.users[ws].nick, "message":t_message})