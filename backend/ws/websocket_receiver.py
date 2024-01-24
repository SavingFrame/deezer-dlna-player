from starlette.websockets import WebSocket

from utils.task_worker.task_worker import PlayerTaskWorker


class WebsocketReceiver:

    def __init__(self, websocket: WebSocket, message: dict, connection_manager):
        self.websocket = websocket
        self.message = message
        self.connection_manager = connection_manager

    async def process_set_device(self, message: dict, websocket: WebSocket):
        from dlna.services.dlna_discovery import upnp_devices_discovery
        from dlna.services.dlna_device import DlnaDevice
        device_udh = message.get('device_udh')
        upnp_device = upnp_devices_discovery.devices[device_udh]
        if getattr(upnp_device, 'subscribers', None):
            upnp_device.subscribers.add(websocket)
        else:
            upnp_device.subscribers = {websocket}
        websocket.device = {
            'device_udh': device_udh,
            'device_url': upnp_device.device_url,
        }
        await DlnaDevice(upnp_device, subscribe=False).notify_specific_subscribers([websocket.uuid])

    async def send_to_worker(self, message: dict):
        message.update({'device': self.websocket.device})
        await PlayerTaskWorker().send_message(message)

    async def handle(self):
        type_message = self.message.get('type')
        match type_message:
            case 'set_device':
                await self.process_set_device(self.message, self.websocket)
            case _:
                await self.send_to_worker(self.message)
