from fastapi import APIRouter
from fastapi.responses import StreamingResponse  # handles streaming input from gemini
from models.schemas import ProductSummaryRequest
from services.generate_product_summary import generate_product_summary
import json
from typing import AsyncGenerator

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

async def stream_product_summaries(request: ProductSummaryRequest) -> AsyncGenerator[bytes, None]:
    for product in request.ranked_products:
        summary = await generate_product_summary(request.query, product, request.chat_history)
        # Send one product summary at a time as a JSON string followed by newline
        yield (json.dumps({
            "product_name": product.product_name,
            "summary": summary
        }) + "\n").encode("utf-8")  # FastAPI StreamingResponse expects bytes

# receive query from user and send response
# use post so data is contained in request body and not in the url
@router.post("/product-summaries")
async def chat_post(request: ProductSummaryRequest):
    return StreamingResponse(stream_product_summaries(request), media_type="application/json")
