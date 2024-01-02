from fastapi import APIRouter
from dlna.api.v1.views import ws

router = APIRouter(prefix='/dlna')
router.include_router(ws.router)
