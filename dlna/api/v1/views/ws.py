from fastapi import APIRouter
from starlette.websockets import WebSocket

from dlna.services.ws_manager import connection_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            await connection_manager.receive(websocket)

    finally:
        await connection_manager.disconnect(websocket)
