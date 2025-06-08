from fastapi import APIRouter
from models.schemas import ProductSummaryRequest
from services.generate_product_summary import generate_product_summary

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# receive query from user and send response
# use post so data is contained in request body and not in the url
@router.post("/product-summaries")
async def chat_post(request: ProductSummaryRequest):
    summaries = []
    # Generate summaries for each ranked product
    for product in request.ranked_products:
        summary = generate_product_summary(product, request.query, request.chat_history)
        summaries.append({
            "product_id": product.product_id,
            "summary": summary
        })

    return summaries # StreamingResponse() from FastAPI function
from fastapi.responses import StreamingResponse # handles streaming input from gemini
