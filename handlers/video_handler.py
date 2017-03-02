import handlers.session_handler as session_handler
from constants import message_types, error_types
from helpers.parse_helper import get_key, MissingKeyError

async def load(ws, message):
    #add permission check
    user = session_handler.users[ws]
    session = user.session

    try:
        video = get_key(message, "video")
    except MissingKeyError as e:
        await message_types.Error(error_type=error_types.missing_key, error=str(e)).send(ws)
        return
    
    session.video = video
    for x in session.users:
        await message_types.LoadVideo(video=video, sender=ws).send(x.ws)

async def status(ws, message):
    #add permission check
    user = session_handler.users[ws]
    session = user.session

    try:
        status = get_key(message, "status")
    except MissingKeyError as e:
        await message_types.Error(error_type=error_types.missing_key, error=str(e)).send(ws)
        return

    valid_statuses = ["play", "pause"]
    if status not in valid_statuses:
        await message_types.Error(error_type=error_types.invalid_status, error="That's not a valid status: {}".status).send(ws)
        return

    if status == "pause":
        session.playing = False
    if status == "play":
        session.playing = True
    
    for x in session.users:
        await message_types.VideoStatus(playing=session.playing, sender=ws).send(x.ws)