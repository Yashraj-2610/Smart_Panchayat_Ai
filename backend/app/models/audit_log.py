from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from datetime import datetime
from ..core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, nullable=False)
    actor_role = Column(String(50))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    details = Column(JSON)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
