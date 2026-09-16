"""
Authentication, RBAC & Privacy API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime

from ...core.database import get_db
from ...core.security import (
    hash_password,
    verify_password,
    create_access_token,
    log_audit_event,
    encrypt_pii,
    decrypt_pii,
    mask_aadhaar
)
from ...core.auth_deps import (
    get_current_user,
    get_current_active_user,
    require_roles
)
from ...models.user import User, UserRole
from ...models.audit_log import AuditLog
from ..schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    AuditLogResponse
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user (Family Head, Sarpanch, Panchayat Admin)
    Returns JWT token and user profile
    """
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_in.username.strip().lower()) |
        (User.email == user_in.email.strip().lower())
    ).first()

    if existing_user:
        if existing_user.username == user_in.username.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

    # Hash the password securely with bcrypt
    hashed_pwd = hash_password(user_in.password)

    new_user = User(
        username=user_in.username.strip().lower(),
        email=user_in.email.strip().lower(),
        hashed_password=hashed_pwd,
        full_name=user_in.full_name.strip(),
        role=user_in.role,
        phone_number=user_in.phone_number,
        preferred_language=user_in.preferred_language,
        is_active=True,
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log registration audit trail
    client_ip = request.client.host if request.client else None
    log_audit_event(
        db=db,
        actor_id=new_user.id,
        actor_role=new_user.role.value,
        action="USER_REGISTRATION",
        resource_type="User",
        resource_id=str(new_user.id),
        details={"username": new_user.username, "role": new_user.role.value},
        ip_address=client_ip
    )

    # Generate JWT access token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "role": new_user.role.value, "username": new_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with username or email and password.
    Returns JWT access token and user information with role.
    """
    identifier = login_data.username_or_email.strip().lower()

    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled. Please contact your Gram Panchayat administrator."
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Log login event
    client_ip = request.client.host if request.client else None
    log_audit_event(
        db=db,
        actor_id=user.id,
        actor_role=user.role.value,
        action="USER_LOGIN",
        resource_type="User",
        resource_id=str(user.id),
        details={"username": user.username, "role": user.role.value},
        ip_address=client_ip
    )

    # Generate access token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value, "username": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current authenticated user's profile"""
    return current_user


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_trail(
    limit: int = 50,
    current_user: User = Depends(require_roles([UserRole.SARPANCH, UserRole.PANCHAYAT_ADMIN, UserRole.SYSTEM_ADMIN])),
    db: Session = Depends(get_db)
):
    """
    View system privacy & security audit trail (Sarpanch & Panchayat Admin only)
    """
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return logs
