from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...api.schemas import SchemeResponse
from ...models.scheme import Scheme
from ...services.rag_service import RAGService

router = APIRouter()

@router.get("/", response_model=List[SchemeResponse])
def list_schemes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all government schemes in the knowledge base"""
    return db.query(Scheme).offset(skip).limit(limit).all()

@router.get("/category/{category}", response_model=List[SchemeResponse])
def get_schemes_by_category(category: str, db: Session = Depends(get_db)):
    """Get schemes by category (Health, Water, Education, etc.)"""
    return db.query(Scheme).filter(Scheme.category == category).all()

@router.get("/search")
def search_schemes(
    query: str = Query(..., min_length=3),
    domain: str = None,
    top_k: int = 5
):
    """
    RAG-based scheme retrieval
    Search for relevant government schemes based on problem description
    """
    results = RAGService.retrieve_relevant_schemes(query, domain, top_k)
    return {
        "query": query,
        "domain": domain,
        "matched_schemes": results
    }

@router.post("/seed")
def seed_schemes_database(db: Session = Depends(get_db)):
    """Seed the database with standard government schemes"""
    RAGService.seed_schemes(db)
    return {"message": "Government schemes database seeded successfully"}
