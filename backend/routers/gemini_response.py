from fastapi import APIRouter, HTTPException, Depends # added  HTTPException, Depends
from models.schemas import QueryRequest
from fastapi.responses import StreamingResponse  # handles streaming input from gemini
# import google.generativeai as genai #added but fails...
import os #added
import json #added
from typing import List, Dict, Any #added
from services.chatbot_response import chatbot_response
from services.product_ranking import product_ranking

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# receive query from user and send response
# use post so data is contained in request body and not in the url
@router.post("/gemini-response")
async def chat_post(request: QueryRequest):
    # Get Product Rankings
    ranked_p = product_ranking(request)
    print(ranked_p)
    # Get gemini response
    return StreamingResponse(chatbot_response(request, ranked_p)) # StreamingResponse() from FastAPI function
from fastapi.responses import StreamingResponse # handles streaming input from gemini