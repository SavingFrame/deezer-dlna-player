import logging
import uuid

import anyio
from fastapi import APIRouter
from starlette.websockets import WebSocket

from ws.websocket_receiver import WebsocketReceiver

router = APIRouter()

logger = logging.getLogger('websockets')


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await WebsocketReceiver.on_connect(websocket)
    # try:
    async with anyio.create_task_group() as task_group:
        async def run_chatroom_ws_receiver() -> None:
            await ws_receiver(websocket=websocket)
            task_group.cancel_scope.cancel()
#
        async def run_chatroom_ws_sender() -> None:
            await ws_sender(websocket=websocket)
            task_group.cancel_scope.cancel()
#
        task_group.start_soon(run_chatroom_ws_receiver)  # noqa
        task_group.start_soon(run_chatroom_ws_sender)  # noqa
    #
    # except* Exception as e_group:
    #     for exception in e_group:
    #         logger.exception("Websocket task failed", exc_info=exception)
    # await ws_sender(websocket=websocket)


async def ws_receiver(websocket):
    async for message in websocket.iter_json():
        await WebsocketReceiver(websocket=websocket, message=message).handle()


async def ws_sender(websocket):
    from main import broadcast
    async with broadcast.subscribe() as subscriber:
        async for event in subscriber:
            receivers = event.headers.get('receivers', 'all')
            logger.debug("In progress to send message to %s", receivers)
            if receivers == 'all' or websocket.uuid in receivers:
                await websocket.send_text(event.message)
                logger.debug("Message sent to %s", websocket.uuid)
