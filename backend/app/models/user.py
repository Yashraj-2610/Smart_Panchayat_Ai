from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from datetime import datetime
import enum
from ..core.database import Base

class UserRole(str, enum.Enum):
    FAMILY_HEAD = "Family Head"
    SARPANCH = "Sarpanch"
    PANCHAYAT_ADMIN = "Panchayat Admin"
    SYSTEM_ADMIN = "System Admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    phone_number = Column(String(15))
    is_active = Column(Boolean, default=True)
    preferred_language = Column(String(5), default="mr")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
