from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class RecommendationStatus(str, enum.Enum):
    GENERATED = "Generated"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    IMPLEMENTED = "Implemented"
    REJECTED = "Rejected"

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(String(50), unique=True, nullable=False, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    priority_score = Column(Float, nullable=False)
    recommendation_text = Column(Text, nullable=False)
    evidence = Column(JSON)  # Stores analysis from agents
    affected_wards = Column(JSON)  # List of ward IDs
    affected_households = Column(Integer)
    suggested_schemes = Column(JSON)  # List of scheme IDs
    estimated_cost = Column(Float)
    estimated_timeline = Column(String(100))
    agent_analysis = Column(JSON)  # Analysis from multiple agents
    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.GENERATED)
    language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    issue = relationship("Issue", back_populates="recommendations")
