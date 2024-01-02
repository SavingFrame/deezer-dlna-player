import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from deezer_integration.api.v1.routes import router as deezer_router
from dlna.api.v1.routes import router as dlna_router
from dlna.services.dlna_discovery import dlna_manager
from dlna.services.message_queue import rabbitmq_service

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


@app.on_event("startup")
async def startup_event():
    await rabbitmq_service.connect()
    asyncio.create_task(dlna_manager.discover_devices())
    asyncio.create_task(dlna_manager.periodical_update_devices())
    asyncio.create_task(rabbitmq_service.consume_messages())
