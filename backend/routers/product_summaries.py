from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse  # handles streaming input from gemini
from models.schemas import ProductSummaryRequest
from services.generate_product_summary import generate_product_summary
import json
from typing import AsyncGenerator
from dependencies.session_history import get_session_history, append_to_session_history

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

async def stream_product_summaries(payload: ProductSummaryRequest, request: Request) -> AsyncGenerator[bytes, None]:
    session_id = request.headers.get("X-Session-ID", "default")
    history = payload.chat_history # use chat history passed from payload
    for product in payload.ranked_products:
        summary = await generate_product_summary(payload.query, product, payload.chat_history)
        product_json = {
            "product_name": product.product_name,
            "summary": summary
        }
        history.append({"role": "vinuca", "content": str(product_json)})
        append_to_session_history(session_id, history)
        # Send one product summary at a time as a JSON string followed by newline
        yield (json.dumps(product_json) + "\n").encode("utf-8")  # FastAPI StreamingResponse expects bytes

# receive query from user and send response
# use post so data is contained in request body and not in the url
@router.post("/product-summaries")
async def chat_post(payload: ProductSummaryRequest, request: Request):
    return StreamingResponse(stream_product_summaries(payload, request), media_type="application/json")
