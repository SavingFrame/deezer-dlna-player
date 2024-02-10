from typing import TYPE_CHECKING

from player_worker.utils import get_dlna_device
from utils.task_worker.task_registry import task

if TYPE_CHECKING:
    from dlna.services.dlna_device import DlnaDevice


@task(queue_key="upnp_listener.event")
@get_dlna_device
async def player_upnp_event(dlna_device: "DlnaDevice", data):
    message = data.get("message")
    service_id = message.get("service_id")
    state_variables = message.get("state_variables")
    await dlna_device.dmr_device._on_queue_event(service_id, state_variables)
