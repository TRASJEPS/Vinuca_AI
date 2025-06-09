from models.schemas import RankedProduct
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.environ['GEMINI_API_KEY']
client = genai.Client(api_key=gemini_key)

# Safety setting and system instructions to ensure customer experience and safety
safety_settings = [types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
]

# Set up the gemini model settings
# Standard Gemini limit of 2048
config = types.GenerateContentConfig(
    temperature=0.9,
    top_p=1,
    top_k=1,
    max_output_tokens=2048,
    safety_settings=safety_settings
)

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
        Generate a helpful summary for this product. Return test if you can see this
        """
    else:
        prompt = f"""
        Given the conversation: {chat_history}
        User query: "{query}"
        Generate a helpful chatbot response.
        """

    summary = client.models.generate_content(
        model="gemini-2.0-flash", 
        config=config,
        contents=prompt)
    return summary.text