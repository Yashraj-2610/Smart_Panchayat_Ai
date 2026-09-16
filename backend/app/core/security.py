"""
Security and Privacy Module for Smart Panchayat AI
- Password hashing & verification with bcrypt
- JWT token generation and validation
- Field-level End-to-End PII encryption (Aadhaar, contact, sensitive demographic data)
- Role-based PII masking
- Audit logging for privacy and compliance
"""
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import jwt
import bcrypt
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from .config import settings
from ..models.audit_log import AuditLog
from ..models.user import User, UserRole

# Derive a 32-byte Fernet key deterministically from SECRET_KEY
_key_bytes = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
_fernet_key = base64.urlsafe_b64encode(_key_bytes)
_cipher_suite = Fernet(_fernet_key)

JWT_ALGORITHM = "HS256"


# ==========================================
# 1. Password Hashing & Verification
# ==========================================

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash"""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# ==========================================
# 2. JWT Token Management
# ==========================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a signed JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate a JWT access token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ==========================================
# 3. End-to-End PII Privacy & Field Encryption
# ==========================================

def encrypt_pii(plain_text: Optional[str]) -> Optional[str]:
    """
    Encrypt sensitive Personally Identifiable Information (PII)
    Uses AES-CBC / Fernet with HMAC authentication
    """
    if not plain_text:
        return plain_text
    try:
        encrypted = _cipher_suite.encrypt(plain_text.encode("utf-8"))
        return encrypted.decode("utf-8")
    except Exception:
        return plain_text


def decrypt_pii(encrypted_text: Optional[str]) -> Optional[str]:
    """
    Decrypt encrypted PII data
    """
    if not encrypted_text:
        return encrypted_text
    try:
        decrypted = _cipher_suite.decrypt(encrypted_text.encode("utf-8"))
        return decrypted.decode("utf-8")
    except Exception:
        # Return as-is if not encrypted (backwards compatibility)
        return encrypted_text


def mask_aadhaar(aadhaar: Optional[str]) -> str:
    """Mask 12-digit Aadhaar number for privacy (XXXX-XXXX-1234)"""
    if not aadhaar:
        return "Not Provided"
    clean = str(aadhaar).replace("-", "").replace(" ", "").strip()
    if len(clean) >= 4:
        return f"XXXX-XXXX-{clean[-4:]}"
    return "XXXX-XXXX-XXXX"


def mask_phone(phone: Optional[str]) -> str:
    """Mask phone number for privacy (+91-XXXXX-98765)"""
    if not phone:
        return "Not Provided"
    clean = str(phone).strip()
    if len(clean) >= 4:
        return f"******{clean[-4:]}"
    return "******"


def mask_income(income: Optional[float]) -> str:
    """Mask exact annual income for privacy"""
    if income is None:
        return "Confidential"
    if income < 50000:
        return "< ₹50,000 (Low Income)"
    elif income < 100000:
        return "₹50,000 - ₹1,00,000 (Middle Income)"
    else:
        return "> ₹1,00,000 (Above Poverty)"


# ==========================================
# 4. Audit Logging for Privacy & RBAC
# ==========================================

def log_audit_event(
    db: Session,
    actor_id: int,
    actor_role: str,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    """Record an audit trail log for security and compliance"""
    try:
        log_entry = AuditLog(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            details=details or {},
            ip_address=ip_address,
            timestamp=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()
        return log_entry
    except Exception:
        db.rollback()
        return None
