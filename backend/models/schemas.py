from pydantic import BaseModel, Field
from typing import List, Optional

# holds one message and sender (user or vinuca).
class ChatMessage(BaseModel):
    sender: str  # "user" or "vinuca"
    message: str

# holds user query and prior chat history.
class QueryRequest(BaseModel):
    query: str
    chat_history: List[ChatMessage]

# contains product identifier plus AI-generated summary.
class ProductSummary(BaseModel):
    product_name: str
    summary: str

# holds chatbot response text and optionally product list.
# THe main front end response model
class QueryResponse(BaseModel):
    response: str
    products: Optional[List[ProductSummary]] = None # Frontend will check this

# The full product details from DB/search
class RankedProduct(BaseModel):
    product_name: str
    score: float
    category: str
    price: str
    details: str
    ingredients: str
    product_link: str

class ProductSummaryRequest(BaseModel):
    query: str
    chat_history: List[ChatMessage]
    ranked_products: List[RankedProduct]