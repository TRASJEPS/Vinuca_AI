from fastapi import APIRouter
from models.schemas import QueryRequest
from services.product_ranking import product_ranking

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

#  receive query from user and send ranked products
@router.post("/ranked-products")
async def chat_post(request: QueryRequest):
    return product_ranking(request)
