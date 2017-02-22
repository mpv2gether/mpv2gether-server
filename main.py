import asyncio
import websockets
import json
from constants import message_types, error_types
import handlers.session_handler as session_handler
import handlers.message_handler as message_handler
from api import send_json

connections = []

async def hello(websocket, path):
    connections.append(websocket)
    while True:
        message = await websocket.recv()
        
        try:
            message = json.loads(message)
        except ValueError:
            await message_types.Error(error_type=error_types.not_json, error="Your input could not be parsed as JSON: {}".format(message)).send(websocket)
        
        if "type" not in message:
            await message_types.Error(error_type=error_types.no_type, error="Your message doesn't have a type.").send(websocket)
            continue
        if message["type"] not in message_types.message_types:
            await message_types.Error(error_type=error_types.invalid_type, error="That's not a valid message type: {}".format(message["type"])).send(websocket)
            continue
        await {
            message_types.create_session: session_handler.create,
            message_types.join_session: session_handler.join,
            message_types.leave_session: session_handler.leave,
            message_types.message: message_handler.message
        }[message["type"]](websocket, message)

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("started server")
asyncio.get_event_loop().run_forever()
