from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.faq import FAQ
from pydantic import BaseModel
from openai import OpenAI
import os

from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter(prefix="/api/faqs", tags=["FAQs"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request model
class FAQCreate(BaseModel):
    question: str
    answer: str

# Response model
class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True

@router.post("/", response_model=FAQResponse)
def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    db_faq = FAQ(question=faq.question, answer=faq.answer)
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq

@router.get("/", response_model=list[FAQResponse])
def get_all_faqs(db: Session = Depends(get_db)):
    return db.query(FAQ).all()

@router.post("/generate")
def generate_faq_answer(question: str = Body(..., embed=True)):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers FAQ questions."},
        {"role": "user", "content": question}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return {"question": question, "generated_answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
