from pydantic import BaseModel
from typing import List

# set up pydantic model
class QueryRequest(BaseModel):
    message: str