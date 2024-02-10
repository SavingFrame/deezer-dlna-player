from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import config
from deezer_integration.api.v1.routes import router as deezer_router
from utils.broadcaster import Broadcast
from ws.views import router as ws_router

broadcast = Broadcast()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deezer_router, prefix='/api/v1', tags=["deezer"])
app.include_router(ws_router, prefix='/api/v1', tags=["ws"])

dictConfig(config.log_config)
# logging.basicConfig(level=logging.DEBUG)
