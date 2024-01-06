# from http import HTTPStatus
# from typing import Mapping
#
# from async_upnp_client.const import ServiceId, NS
# from async_upnp_client.event_handler import UpnpEventHandler, _LOGGER
# import defusedxml.ElementTree as DET
#
# from dlna.services.dlna_device import DlnaDevice
# from dlna.utils import send_message_to_clients
#
#
# class CustomUpnpEventHandler(UpnpEventHandler):
#     async def handle_notify(self, headers: Mapping[str, str], body: str) -> HTTPStatus:
#         if "NT" not in headers or "NTS" not in headers:
#             return HTTPStatus.BAD_REQUEST
#
#         if (
#             headers["NT"] != "upnp:event"
#             or headers["NTS"] != "upnp:propchange"
#             or "SID" not in headers
#         ):
#             return HTTPStatus.PRECONDITION_FAILED
#
#         sid: ServiceId = headers["SID"]
#         service = self._subscriptions.get(sid)
#
#         # SID not known yet? store it in the backlog
#         # Some devices don't behave nicely and send events before the SUBSCRIBE call is done.
#         if not service:
#             _LOGGER.debug("Storing NOTIFY in backlog for SID: %s", sid)
#             self._backlog[sid] = (
#                 headers,
#                 body,
#             )
#
#             return HTTPStatus.OK
#
#         # decode event and send updates to service
#         changes = {}
#         stripped_body = body.rstrip(" \t\r\n\0")
#         el_root = DET.fromstring(stripped_body)
#         for el_property in el_root.findall("./event:property", NS):
#             for el_state_var in el_property:
#                 name = el_state_var.tag
#                 value = el_state_var.text or ""
#                 changes[name] = value
#
#         # send changes to service
#         service.notify_changed_state_variables(changes)
#         device = service.device
#         dlna_device = DlnaDevice(upnp_device=device, subscribe=False)
#         info = await dlna_device.player_info()
#         await send_message_to_clients(info, type='player')
#         return HTTPStatus.OK
