from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # handles CORS
from contextlib import asynccontextmanager
from routers import gemini_response, ranked_products, product_summaries, is_requesting_products

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
    
app.include_router(gemini_response.router)
app.include_router(is_requesting_products.router)
app.include_router(ranked_products.router)
app.include_router(product_summaries.router)
