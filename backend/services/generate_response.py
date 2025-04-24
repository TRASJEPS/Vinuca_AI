from fastapi.responses import StreamingResponse # handles streaming input from gemini
from typing import List
import requests
import asyncio

import os
from google import genai
from dotenv import load_dotenv

# loads key value pairs from my .env file
load_dotenv()

gemini_key = os.environ['GEMINI_API_KEY']
client = genai.Client(api_key=gemini_key)

async def chatbot_response(query):
    async for chunk in await client.aio.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[query.message]):
        if chunk.text:
            print(chunk.text)
            yield chunk.text
    '''return client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[query.message])'''