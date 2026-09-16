"""
Authentication & Role-Based Access Control (RBAC) Dependencies
"""
from typing import List, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .security import decode_access_token
from ..models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False
)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate JWT token from Bearer header or OAuth2Scheme.
    Returns the authenticated User model.
    """
    # Check Authorization header if oauth2_scheme didn't capture it
    actual_token = token
    if not actual_token and authorization:
        if authorization.startswith("Bearer "):
            actual_token = authorization.split("Bearer ")[1].strip()
        else:
            actual_token = authorization.strip()

    if not actual_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(actual_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account no longer exists"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated. Contact Gram Panchayat administrator."
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure the user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_optional_user(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Optional user authentication for public/semi-public endpoints"""
    actual_token = token
    if not actual_token and authorization:
        if authorization.startswith("Bearer "):
            actual_token = authorization.split("Bearer ")[1].strip()
        else:
            actual_token = authorization.strip()

    if not actual_token:
        return None

    payload = decode_access_token(actual_token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return db.query(User).filter(User.id == int(user_id)).first()


def require_roles(allowed_roles: List[UserRole]):
    """
    Dependency factory to enforce Role-Based Access Control (RBAC)
    Example: Depends(require_roles([UserRole.SARPANCH, UserRole.PANCHAYAT_ADMIN]))
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            role_names = ", ".join([r.value for r in allowed_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of the following roles: {role_names}. Your role is: {current_user.role.value}."
            )
        return current_user

    return role_checker
