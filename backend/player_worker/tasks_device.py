from dlna.services.dlna_device import DlnaDevice
from player_worker.utils import get_dlna_device
from utils.task_worker.task_registry import task


@task(queue_key='device.set_volume')
@get_dlna_device
async def player_set_volume(dlna_device: DlnaDevice, data):
    volume = data.get('message')
    await dlna_device.set_volume(volume)
