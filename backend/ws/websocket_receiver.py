import uuid

from starlette.websockets import WebSocket

from utils.task_worker.task_worker import PlayerTaskWorker


class WebsocketReceiver:

    def __init__(self, websocket: WebSocket, message: dict):
        self.websocket = websocket
        self.message = message

    @classmethod
    async def send_to_worker(cls, message: dict):
        await PlayerTaskWorker().send_message(message)

    async def handle(self):
        # type_message = self.message.get('type')
        self.message['client_uuid'] = self.websocket.uuid
        await self.send_to_worker(self.message)

    @classmethod
    async def on_connect(cls, websocket: WebSocket) -> None:
        websocket.uuid = str(uuid.uuid4())
        message = {'type': 'device.get_devices', 'receivers': [websocket.uuid]}
        await cls.send_to_worker(message)
        return

    @classmethod
    async def on_disconnect(cls, websocket: WebSocket) -> None:
        message = {'type': 'device.unsubscribe', 'client_uuid': [websocket.uuid]}
        await cls.send_to_worker(message)
        return
