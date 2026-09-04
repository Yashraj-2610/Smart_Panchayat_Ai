from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class IssueCategory(str, enum.Enum):
    WATER = "Water"
    SANITATION = "Sanitation"
    ROAD = "Road & Infrastructure"
    HEALTH = "Health"
    EDUCATION = "Education"
    AGRICULTURE = "Agriculture"
    ELECTRICITY = "Electricity"
    OTHER = "Other"

class IssueStatus(str, enum.Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"

class IssuePriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(String(50), unique=True, nullable=False, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    category = Column(Enum(IssueCategory), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(IssueStatus), default=IssueStatus.SUBMITTED)
    priority = Column(Enum(IssuePriority), default=IssuePriority.MEDIUM)
    affected_count = Column(Integer, default=1)
    language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    household = relationship("Household", back_populates="issues")
    recommendations = relationship("AIRecommendation", back_populates="issue")
