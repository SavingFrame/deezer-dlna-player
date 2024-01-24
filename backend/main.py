import asyncio
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from deezer_integration.api.v1.routes import router as deezer_router
from dlna.services.dlna_discovery import upnp_devices_discovery
from dlna.views import router as dlna_router
from ws.views import router as ws_router
from ws.message_queue import rabbitmq_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deezer_router, prefix='/api/v1', tags=["deezer"])
app.include_router(dlna_router, prefix='/api/v1', tags=["dlna"])
app.include_router(ws_router, prefix='/api/v1', tags=["ws"])

logging.basicConfig(level="INFO")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(upnp_devices_discovery.discover_devices())
    asyncio.create_task(upnp_devices_discovery.periodical_update_devices())
    asyncio.create_task(rabbitmq_service.consume_messages())
