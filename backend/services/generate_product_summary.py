from models.schemas import RankedProduct
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.environ['GEMINI_API_KEY']
client = genai.Client(api_key=gemini_key)

async def generate_product_summary(query: str, product: dict | None, chat_history: list) -> str:
    """
    Generate a summary or response from the Gemini model.
    If product is None, generate a general chatbot reply.
    Else, generate a product summary tailored to the query.
    """

    if product:
        prompt = f"""
        Given the conversation: {chat_history}
        User query: "{query}"
        Product info: {product}
        Generate a helpful summary for this product.
        """
    else:
        prompt = f"""
        Given the conversation: {chat_history}
        User query: "{query}"
        Generate a helpful chatbot response.
        """

    summary = await client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt)
    return 