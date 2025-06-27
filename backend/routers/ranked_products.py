from fastapi import APIRouter, Request
from models.schemas import QueryRequest
from services.product_ranking import product_ranking
from dependencies.session_history import append_to_session_history

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

#  receive query from user and send ranked products
@router.post("/ranked-products")
async def chat_post(payload: QueryRequest, request: Request):
    session_id = request.headers.get("X-Session-ID", "default")
    ranked_products = product_ranking(payload)
    history = payload.chat_history
    history.append({"role": "vinuca", "content": str(ranked_products)})
    append_to_session_history(session_id, history)
    return ranked_products
