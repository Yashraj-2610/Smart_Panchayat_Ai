from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from datetime import datetime
import enum
from ..core.database import Base

class SchemeCategory(str, enum.Enum):
    HEALTH = "Health"
    EDUCATION = "Education"
    AGRICULTURE = "Agriculture"
    WATER = "Water & Sanitation"
    INFRASTRUCTURE = "Infrastructure"
    SOCIAL_WELFARE = "Social Welfare"
    HOUSING = "Housing"
    EMPLOYMENT = "Employment"

class SchemeLevel(str, enum.Enum):
    CENTRAL = "Central"
    STATE = "State"
    DISTRICT = "District"

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(300), nullable=False)
    name_hindi = Column(String(300))
    name_marathi = Column(String(300))
    category = Column(Enum(SchemeCategory), nullable=False)
    level = Column(Enum(SchemeLevel), nullable=False)
    description = Column(Text, nullable=False)
    description_hindi = Column(Text)
    description_marathi = Column(Text)
    eligibility_criteria = Column(Text)
    benefits = Column(Text)
    application_process = Column(Text)
    official_link = Column(String(500))
    contact_details = Column(String(500))
    document_path = Column(String(500))  # Path to full scheme document
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
