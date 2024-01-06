from dlna.services.dlna_device import DlnaDevice
from library.track import Track
from player_control.utils import get_dlna_device
from utils.task_worker.task_registry import task


@task(queue_key='player.play')
@get_dlna_device
async def player_play(dlna_device: DlnaDevice, data):
    track_id = data.get('message')
    print(dlna_device, data)
    await Track.from_deezer_by_id(track_id, dlna_device).play()
