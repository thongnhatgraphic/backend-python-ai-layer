from fastapi import APIRouter

router = APIRouter()


@router.post("/runs/{run_id}/confirm")
async def confirm():
    return
