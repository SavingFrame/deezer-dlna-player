import json
import logging

from main import broadcast

logger = logging.getLogger("websockets")


async def send_message_to_websockets(message: dict | list, websockets_uuid: list[str] = None):
    message = json.dumps(message)
    logger.debug(f"Send message to websockets: {message}")
    if not websockets_uuid:
        websockets_uuid = "all"
    await broadcast.publish(message=message, headers={"receivers": websockets_uuid})
