from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.faq import FAQ
from pydantic import BaseModel

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

