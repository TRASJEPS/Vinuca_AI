from pydantic import BaseModel
from typing import List, Optional

# holds user query (old) for gemini-response endpoint
class UserQuery(BaseModel):
    message: str

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
    product_id: str
    summary: str

# holds chatbot response text and optionally product list.
class QueryResponse(BaseModel):
    response: str
    products: Optional[List[ProductSummary]] = None

class RankedProduct(BaseModel):
    product_id: str
    name: str
    price: float
    top_active_ingredients: List[str]
    product_link: str
    recommendation: str

class ProductSummaryRequest(BaseModel):
    query: str
    chat_history: List[ChatMessage]
    ranked_products: List[RankedProduct]