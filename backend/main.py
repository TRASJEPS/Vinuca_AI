from typing import Union

from fastapi import FastAPI
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

gemini_key = os.environ['GEMINI_API_KEY']
print(gemini_key)

client = genai.Client(api_key=gemini_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["How does AI work?"])
print(response.text)

@app.get("/")
def read_root():
    return {"Key": response}


'''import os
import google.generativeai as genai
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
app = FastAPI(
    Title="AI Chat API",
    docs_url='/',
    description="This API allows you to chat with an AI model using WebSocket connections.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/chat", tags=["Chat"])
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for handling chat messages.

    This WebSocket endpoint allows clients to send messages to the AI model
    and receive streamed responses.

    To use this endpoint, establish a WebSocket connection to `/ws`.

    - Send a message to the WebSocket.
    - Receive a response from the AI model.
    - If the message "exit" is sent, the chat session will end.
    """
    await websocket.accept()
    chat = model.start_chat(history=[])
    try:
        while True:
            data = await websocket.receive_text()
            if data.lower().startswith("you: "):
                user_message = data[5:]
                if user_message.lower() == "exit":
                    await websocket.send_text("AI: Ending chat session.")
                    break
                response = chat.send_message(user_message, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                await websocket.send_text("AI: " + full_response)
            else:
                await websocket.send_text("AI: Please start your message with 'You: '")
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()'''
