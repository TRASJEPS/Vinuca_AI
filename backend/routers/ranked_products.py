from fastapi import APIRouter
from models.schemas import QueryRequest
from services.generate_response import chatbot_response
from services.product_ranking import product_ranking

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

#  receive query from user and send ranked products
@router.post("/ranked-products")
async def chat_post(query: QueryRequest):
    return product_ranking(query.query)
