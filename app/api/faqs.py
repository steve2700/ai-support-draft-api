from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.faq import FAQ
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/faqs", tags=["FAQs"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FAQCreate(BaseModel):
    question: str
    answer: str

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
def get_all_faqs(
    db: Session = Depends(get_db), 
    limit: int = 10, 
    offset: int = 0, 
    search: str | None = None
):
    query = db.query(FAQ)
    if search:
        query = query.filter(FAQ.question.ilike(f"%{search}%"))
    faqs = query.offset(offset).limit(limit).all()
    return faqs

@router.post("/generate", response_model=FAQResponse)
def generate_faq_answer(
    question: str = Body(..., embed=True), 
    db: Session = Depends(get_db)
):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Check if question already exists in DB
    existing = db.query(FAQ).filter(FAQ.question == question).first()
    if existing:
        return existing

    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers FAQ questions."},
        {"role": "user", "content": question}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            store=True,
        )
        answer = completion.choices[0].message.content.strip()

        # Save to DB
        new_faq = FAQ(question=question, answer=answer)
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)

        return new_faq
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

