from typing import Iterable

from utils.broadcaster.utils import send_message_to_websockets


async def send_message_to_clients(message: dict | list, type: str):
    if type not in ['player', 'devices']:
        raise ValueError('Invalid message type')
    message = {
        'type': type,
        'message': message
    }
    await send_message_to_websockets(message)


async def send_message_to_specific_clients(message: dict | list, type: str, websockets_uuid: Iterable[str]):
    if not websockets_uuid:
        return
    if type not in ['player', 'devices']:
        raise ValueError('Invalid message type')
    message = {
        'type': type,
        'message': message
    }
    await send_message_to_websockets(message, list(websockets_uuid))
