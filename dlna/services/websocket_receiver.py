# from starlette.websockets import WebSocket
#
#
# class WebsocketReceiver:
#
#     def __init__(self, websocket: WebSocket, message: dict, connection_manager):
#         self.websocket = websocket
#         self.message = message
#         self.connection_manager = connection_manager
#
#     async def process_set_device(self, message: dict, websocket: WebSocket):
#         websocket.device = message.get('device_udh')
#         print('done')
#         print(websocket.device)
#         for connection in self.connection_manager.active_connections:
#             print(connection.device)
#
#     async def handle(self):
#         type_message = self.message.get('type')
#         print('handle', type_message)
#         match type_message:
#             case 'set_device':
#                 await self.process_set_device(self.message, self.websocket)
#             case _:
#                 pass
