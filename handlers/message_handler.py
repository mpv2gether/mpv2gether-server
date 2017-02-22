import handlers.session_handler as session_handler
from constants import message_types, error_types
from helpers.parse_helper import get_key, MissingKeyError

async def message(ws, w_message):
    if not ws in session_handler.users:
        await message_types.Error(error_type=error_types.not_in_session, error="You're not in a session, so you can't send a message.").send(ws)
        return
    try:
        t_message = get_key(w_message, "message")
    except MissingKeyError as e:
        await message_types.Error(error_type=error_types.missing_key, error=str(e)).send(ws)
        return
    for x in session_handler.users[ws].session.users:
        await message_types.TMessage(message=t_message, sender=ws).send(x.ws)
