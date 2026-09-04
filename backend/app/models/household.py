from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class HouseholdType(str, enum.Enum):
    APL = "APL"  # Above Poverty Line
    BPL = "BPL"  # Below Poverty Line
    ANTODAYA = "Antodaya"

class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(String(50), unique=True, nullable=False, index=True)
    head_name = Column(String(200), nullable=False)
    head_age = Column(Integer)
    head_gender = Column(String(20))
    head_occupation = Column(String(100))
    contact_number = Column(String(15))
    address = Column(String(500))
    ward_id = Column(Integer, ForeignKey("wards.id"), nullable=False)
    household_type = Column(Enum(HouseholdType), default=HouseholdType.APL)
    total_members = Column(Integer, default=0)
    annual_income = Column(Float)
    ration_card_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ward = relationship("Ward", back_populates="households")
    members = relationship("FamilyMember", back_populates="household", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="household")
