import json
from typing import Set

from starlette.websockets import WebSocket

from dlna.services.websocket_receiver import WebsocketReceiver


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print("Connected: ", websocket, " Total connections: ", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Disconnected: ", websocket, " Total connections: ", len(self.active_connections))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def _receive(self, websocket: WebSocket):
        data = await websocket.receive_text()
        return json.loads(data)

    async def receive(self, websocket: WebSocket):
        data = await self._receive(websocket)
        await WebsocketReceiver(websocket, data, connection_manager).handle()


connection_manager = ConnectionManager()
