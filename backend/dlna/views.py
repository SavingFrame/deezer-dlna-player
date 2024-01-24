from fastapi import APIRouter

router = APIRouter(prefix='/dlna')


@router.get("/notify")
def dlna_notify():
    return dict(
        status="success",
        message="DLNA Notify"
    )
