import uuid

from starlette.websockets import WebSocket

from utils.task_worker.senders import send_message_to_task_worker


class WebsocketReceiver:

    def __init__(self, websocket: WebSocket, message: dict):
        self.websocket = websocket
        self.message = message


    async def handle(self):
        # type_message = self.message.get('type')
        self.message['client_uuid'] = self.websocket.uuid
        await send_message_to_task_worker(self.message)

    @classmethod
    async def on_connect(cls, websocket: WebSocket) -> None:
        websocket.uuid = str(uuid.uuid4())
        message = {'type': 'device.get_devices', 'receivers': [websocket.uuid]}
        await send_message_to_task_worker(message)
        return

    @classmethod
    async def on_disconnect(cls, websocket: WebSocket) -> None:
        message = {'type': 'device.unsubscribe', 'client_uuid': [websocket.uuid]}
        await send_message_to_task_worker(message)
        return
