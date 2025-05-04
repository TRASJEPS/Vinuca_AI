from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # handles CORS
from fastapi.responses import StreamingResponse # handles streaming input from gemini
from pydantic import BaseModel # for data validation and parsing. Checks missing, incorrect, and bad data at entry point https://docs.pydantic.dev/latest/
from typing import List
import requests
import asyncio

import os
from google import genai
from dotenv import load_dotenv

from services.generate_response import chatbot_response

# loads key value pairs from my .env file
# load_dotenv()

# start fastAPI app
app = FastAPI()

# Add CORS middleware to allow web pages to make requests
# currently allows everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# receive query from user and send response
# use post so data is contained in request body and not in the url

# set up pydantic model
class QueryRequest(BaseModel):
    message: str

@app.post("/api/gemini-response")
async def chat_post(query: QueryRequest):
    
    # step 1: Query asking for products or not?
    # step 2: If so, get product rankings
    # step 3: Ask for gemini results
    return StreamingResponse(chatbot_response(query)) # StreamingResponse() from FastAPI function
    # data = {"message": query.message}