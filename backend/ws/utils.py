from ws.message_queue import rabbitmq_service


async def send_message_to_clients(message: dict | list, type: str):
    if type not in ['player', 'devices']:
        raise ValueError('Invalid message type')
    message = {
        'type': type,
        'message': message
    }
    await rabbitmq_service.broadcast_send(message)


async def send_message_to_specific_clients(message: dict | list, type: str, websockets_uuid: list[str]):
    if not websockets_uuid:
        return
    if type not in ['player', 'devices']:
        raise ValueError('Invalid message type')
    message = {
        'type': type,
        'message': message
    }
    await rabbitmq_service.send_to_device(message, websockets_uuid)
