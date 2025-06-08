from fastapi import APIRouter
from models.schemas import UserQuery
from fastapi.responses import StreamingResponse  # handles streaming input from gemini
from services.generate_response import chatbot_response
from services.product_ranking import product_ranking

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# receive query from user and send response
# use post so data is contained in request body and not in the url
@router.post("/gemini-response")
async def chat_post(query: UserQuery):
    # Get Product Rankings
    ranked_p = product_ranking(query)
    print(ranked_p)
    # Get gemini response
    return StreamingResponse(chatbot_response(query, ranked_p)) # StreamingResponse() from FastAPI function
from fastapi.responses import StreamingResponse # handles streaming input from gemini
