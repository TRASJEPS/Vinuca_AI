from pydantic import BaseModel, Field
from typing import List, Optional

# holds one message and sender (user or vinuca).
class ChatMessage(BaseModel):
    role: str  # "user" or "vinuca"
    content: str

# holds user query and prior chat history.
class QueryRequest(BaseModel):
    query: str
    chat_history: List[ChatMessage]

# contains product identifier plus AI-generated summary.
class ProductSummary(BaseModel):
    product_name: str
    summary: str

# holds chatbot response text and optionally product list.
class QueryResponse(BaseModel):
    response: str
    products: Optional[List[ProductSummary]] = None

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