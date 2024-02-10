from dlna.services.dlna_device import DlnaDevice
from player_worker.utils import get_dlna_device
from utils.task_worker.task_registry import task


@task(queue_key="internal.set_next_track")
@get_dlna_device
async def player_set_next_track(dlna_device: DlnaDevice, data):
    player_queue = await dlna_device.get_player_queue()
    await player_queue.set_next_song()
