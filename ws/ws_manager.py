import json
import uuid
from typing import Set

from starlette.websockets import WebSocket

from ws.websocket_receiver import WebsocketReceiver


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        from dlna.services.dlna_discovery import upnp_devices_discovery
        await websocket.accept()
        websocket.uuid = uuid.uuid4()
        self.active_connections.add(websocket)
        print("Connected: ", websocket, "uuid", websocket.uuid, " Total connections: ", len(self.active_connections))
        await upnp_devices_discovery.update_device_for_client(websocket.uuid)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Disconnected: ", websocket, "uuid", websocket.uuid, " Total connections: ", len(self.active_connections))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_to(self, message: str, websockets_uuid: list[str | uuid.UUID]):
        for connection in self.active_connections:
            if str(connection.uuid) in websockets_uuid:
                await connection.send_text(message)

    async def _receive(self, websocket: WebSocket):
        data = await websocket.receive_text()
        return json.loads(data)

    async def receive(self, websocket: WebSocket):
        data = await self._receive(websocket)
        await WebsocketReceiver(websocket, data, connection_manager).handle()


connection_manager = ConnectionManager()
