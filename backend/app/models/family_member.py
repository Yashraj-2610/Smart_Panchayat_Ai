from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class Gender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class EducationLevel(str, enum.Enum):
    ILLITERATE = "Illiterate"
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    HIGHER_SECONDARY = "Higher Secondary"
    GRADUATE = "Graduate"
    POSTGRADUATE = "Postgraduate"

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    full_name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    relation_to_head = Column(String(50))
    date_of_birth = Column(Date)
    aadhar_number = Column(String(12), unique=True, nullable=True)
    education_level = Column(Enum(EducationLevel))
    occupation = Column(String(100))
    is_employed = Column(Boolean, default=False)
    is_student = Column(Boolean, default=False)
    has_health_issues = Column(Boolean, default=False)
    health_issue_description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    household = relationship("Household", back_populates="members")
