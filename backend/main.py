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
from services.product_ranking import product_ranking
from services.data_cleaning import data_cleaning

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


# Call data cleaning function on startup
@app.on_event("startup")
async def startup_event():
    cleaned_data = data_cleaning()
    app.state.cleaned_data = cleaned_data # store data in app state. This data can be used across the app
    print("data cleaning completed")

# set up pydantic model
class QueryRequest(BaseModel):
    message: str

# receive query from user and send response
# use post so data is contained in request body and not in the url
@app.post("/api/gemini-response")
async def chat_post(query: QueryRequest):
    # Get Feature Ranking
    #await asyncio.to_thread(print, product_ranking(query, app.state.cleaned_data))
    ranked_p = product_ranking(query, app.state.cleaned_data)
    print(ranked_p)
    # Get gemini product results
    return StreamingResponse(chatbot_response(query, ranked_p)) # StreamingResponse() from FastAPI function
    # data = {"message": query.message}