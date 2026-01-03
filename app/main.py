
from fastapi import FastAPI
from app.routers.books import router as book_router

app = FastAPI(title="Book Management API")

app.include_router(book_router)
