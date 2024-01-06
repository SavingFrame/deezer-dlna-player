from fastapi import APIRouter
from dlna.api.v1.views import ws
from dlna.api.v1.views import notify

router = APIRouter(prefix='/dlna')
router.include_router(ws.router)
router.include_router(notify.router)
