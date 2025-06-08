import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from models.schemas import QueryRequest

# loads key value pairs from my .env file
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
system_instructions = f"""You are an AI Hair Care Assistant named Vinuca. You must maintain this persona at all times." \
                        "Do not give the user a recommendation unless their query talks about their hair care preferences. " \
                        "Do not answer anything that is not related to cosmetics. " \
                        "When giving a user recommendations, always give them three recommendations at a time. " \
                        "List the product's attributes by the name, price, top active ingredients, product link, each attribute must be on a new line and end with a one to three sentence summary on why you recommend this product. " \
                        "A product recommendation should always start with the product name and should be numbered. " \
                        "All product recommendations should have the product name in bold and each attribute for the recommendation such as price, top active ingredients, product link, and recommendation should be sub-bullet points. " \
                        "The sub bullet points should all be on new lines."\
                        "To format the products better, please put each product recommendation into a separate div container that holds the text descriptions you are formatting. " \
                        "Each div should take up one third of the chat bot window as you generate. " \
                        "When providing the link, always give them whatever links you have." \
                        "You must decide when to ask questions, give them the best products, and when they are simply chatting with you. " \
                        "I'll give you their query and context and you'll return the answer. " \
                        "If they ask for more recommendations, give them the recommendations based on the previous list of products that were shared. " \
                        "Use the query, chat history, any previous recommendations I have given you, and the product details to return your answer. " \
                    """

# Set up the gemini model settings
# Standard Gemini limit of 2048
config = types.GenerateContentConfig(
    temperature=0.9,
    top_p=1,
    top_k=1,
    max_output_tokens=2048,
    safety_settings=safety_settings,
    system_instruction=system_instructions,
)

# Load embedding model and move to GPU if available
# Chatbot feature
async def chatbot_response(request: QueryRequest, ranked_p):
    prompt = f"Query: {request.query}\nRanked Products:{ranked_p}"
    async for chunk in await client.aio.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=config,
        ):
        if chunk.text:
            print(chunk.text)
            yield chunk.text