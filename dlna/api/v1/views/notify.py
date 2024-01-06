from fastapi import APIRouter

router = APIRouter()


@router.get("/notify")
def dlna_notify():
    return dict(
        status="success",
        message="DLNA Notify"
    )
