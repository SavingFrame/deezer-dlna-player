import json

from dlna.services.message_queue import rabbitmq_service


async def send_message_to_clients(message: dict | list, type: str):
    print('send message to clients')
    if type not in ['player', 'devices']:
        raise ValueError('Invalid message type')
    message = {
        'type': type,
        'message': message
    }
    message = json.dumps(message)
    await rabbitmq_service.publish_message(message)
