import json

async def send_json(target, type, data):
    output = json.dumps({**{"type":type}, **data})
    await target.send(output)