from player_worker.utils import get_dlna_device
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dlna.services.dlna_device import DlnaDevice


@get_dlna_device
async def player_upnp_event(dlna_device: 'DlnaDevice', data):
    message = data.get('message')
    service_id = message.get('service_id')
    state_variables = message.get('state_variables')
    dlna_device.dmr_device._on_queue_event(service_id, state_variables)