import uuid

import anyio
from fastapi import APIRouter
from starlette.websockets import WebSocket

# from ws.ws_manager import connection_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket.uuid = str(uuid.uuid4())
    async with anyio.create_task_group() as task_group:
        async def run_chatroom_ws_receiver() -> None:
            await ws_receiver(websocket=websocket)
            task_group.cancel_scope.cancel()

        async def run_chatroom_ws_sender() -> None:
            await ws_sender(websocket=websocket)
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_chatroom_ws_receiver)  # noqa
        task_group.start_soon(run_chatroom_ws_sender)  # noqa


async def ws_receiver(websocket):
    from main import broadcast
    async for message in websocket.iter_text():
        await broadcast.publish(message=message, headers={'receivers': [websocket.uuid]})


async def ws_sender(websocket):
    from main import broadcast
    async with broadcast.subscribe() as subscriber:
        async for event in subscriber:
            receivers = event.headers.get('receivers', 'all')
            if receivers == 'all' or websocket.uuid in receivers:
                await websocket.send_text(event.message)
