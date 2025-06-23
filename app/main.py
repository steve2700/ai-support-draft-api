from fastapi import FastAPI
from app.api import faqs

app = FastAPI(title="AI Support Draft API")

app.include_router(faqs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Support Draft Generator API!"}

