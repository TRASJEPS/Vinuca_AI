from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies.session_history import get_session_history
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

@router.get("/session-history/{session_id}")
async def get_history(session_id: str):
    """
    Retrieve the session history for a given session ID.
    """
    history = get_session_history(session_id)
    if not history:
        return JSONResponse(status_code=400, content={"message": "Session history not found."})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(history))
