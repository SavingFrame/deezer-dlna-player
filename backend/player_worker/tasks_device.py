from dlna.services.dlna_device import DlnaDevice
from player_worker.utils import get_dlna_device
from utils.task_worker.task_registry import task
from dlna.services.dlna_discovery import upnp_devices_discovery


@task(queue_key='device.set_volume')
@get_dlna_device
async def player_set_volume(dlna_device: DlnaDevice, data):
    volume = data.get('message')
    await dlna_device.set_volume(volume)


@task(queue_key='device.get_devices')
async def send_devices_to_websocket(data):
    receivers = data.get('receivers')
    await upnp_devices_discovery.send_devices_to_websockets(receivers)


@task(queue_key='device.subscribe')
@get_dlna_device
async def set_device(dlna_device: DlnaDevice, data):
    client_uuid = data.get('client_uuid')
    await dlna_device.subscribe(client_uuid)
    await dlna_device.notify_subscribers()


@task(queue_key='device.unsubscribe')
async def remove_device(data):
    client_uuid = data.get('client_uuid')
    await DlnaDevice.unsubscribe_all(client_uuid)
