import json

from main import broadcast


async def send_message_to_websockets(message: dict | list, websockets_uuid: list[str] = None):
    message = json.dumps(message)
    if not websockets_uuid:
        websockets_uuid = 'all'
    await broadcast.publish(message=message, headers={'receivers': websockets_uuid})
