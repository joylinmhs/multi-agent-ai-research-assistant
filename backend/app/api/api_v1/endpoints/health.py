from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def status():
    return {"status": "healthy", "service": "Research Assistant API"}
