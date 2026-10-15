"""
Privacy & Access Control Layer
Enforces granular permission levels based on user role and data sensitivity
No .env changes needed - all configured programmatically
"""

from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Callable
from functools import wraps
from ..models.user import User, UserRole
from .security import log_audit_event
import logging

logger = logging.getLogger(__name__)

# Privacy Level Definitions
PRIVACY_LEVELS = {
    "PUBLIC": 1,
    "INTERNAL": 2,
    "CONFIDENTIAL": 3,
    "RESTRICTED": 4,
}

# Role-Based Access Mapping
ROLE_PRIVACY_ACCESS = {
    UserRole.FAMILY_HEAD: [PRIVACY_LEVELS["PUBLIC"], PRIVACY_LEVELS["INTERNAL"]],
    UserRole.PANCHAYAT_ADMIN: [PRIVACY_LEVELS["PUBLIC"], PRIVACY_LEVELS["INTERNAL"], PRIVACY_LEVELS["CONFIDENTIAL"]],
    UserRole.SARPANCH: [PRIVACY_LEVELS["PUBLIC"], PRIVACY_LEVELS["INTERNAL"], PRIVACY_LEVELS["CONFIDENTIAL"], PRIVACY_LEVELS["RESTRICTED"]],
    UserRole.SYSTEM_ADMIN: [PRIVACY_LEVELS["PUBLIC"], PRIVACY_LEVELS["INTERNAL"], PRIVACY_LEVELS["CONFIDENTIAL"], PRIVACY_LEVELS["RESTRICTED"]],
}

# Operation Permissions
OPERATION_PERMISSIONS = {
    "view_own_data": [UserRole.FAMILY_HEAD, UserRole.PANCHAYAT_ADMIN, UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "edit_own_data": [UserRole.FAMILY_HEAD, UserRole.PANCHAYAT_ADMIN, UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "report_issue": [UserRole.FAMILY_HEAD, UserRole.PANCHAYAT_ADMIN, UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "view_all_households": [UserRole.PANCHAYAT_ADMIN, UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "view_audit_logs": [UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "manage_users": [UserRole.SYSTEM_ADMIN],
    "view_encrypted_pii": [UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
    "generate_reports": [UserRole.PANCHAYAT_ADMIN, UserRole.SARPANCH, UserRole.SYSTEM_ADMIN],
}


def check_privacy_access(user: User, required_level: str) -> bool:
    """Check if user role can access data at required privacy level"""
    required_level_num = PRIVACY_LEVELS.get(required_level, PRIVACY_LEVELS["PUBLIC"])
    accessible_levels = ROLE_PRIVACY_ACCESS.get(user.role, [])

    return required_level_num in accessible_levels


def check_operation_permission(user: User, operation: str) -> bool:
    """Check if user role has permission for specific operation"""
    allowed_roles = OPERATION_PERMISSIONS.get(operation, [])
    return user.role in allowed_roles


def require_privacy_level(required_level: str):
    """Decorator to enforce privacy level access"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user from dependency
            current_user = kwargs.get("current_user")
            db = kwargs.get("db")
            request = kwargs.get("request")

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if not check_privacy_access(current_user, required_level):
                # Log security event
                if db:
                    log_audit_event(
                        db=db,
                        actor_id=current_user.id,
                        actor_role=current_user.role.value,
                        action="ACCESS_DENIED",
                        resource_type="Privacy Level",
                        resource_id=required_level,
                        details={"required_level": required_level},
                        ip_address=request.client.host if request and request.client else None
                    )

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. This resource requires {required_level} level access."
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def require_permission(operation: str):
    """Decorator to enforce operation permissions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            db = kwargs.get("db")
            request = kwargs.get("request")

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if not check_operation_permission(current_user, operation):
                if db:
                    log_audit_event(
                        db=db,
                        actor_id=current_user.id,
                        actor_role=current_user.role.value,
                        action="PERMISSION_DENIED",
                        resource_type="Operation",
                        resource_id=operation,
                        details={"operation": operation},
                        ip_address=request.client.host if request and request.client else None
                    )

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You do not have permission to {operation}"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def mask_sensitive_field(value: str, field_type: str = "default") -> str:
    """Mask sensitive fields in responses"""
    if not value:
        return "Not provided"

    masks = {
        "aadhaar": lambda v: f"XXXX-XXXX-{v[-4:] if len(v) >= 4 else 'XXXX'}",
        "phone": lambda v: f"XXXXXX{v[-4:] if len(v) >= 4 else 'XXXX'}",
        "email": lambda v: f"{v[0]}***@{v.split('@')[1] if '@' in v else 'email.com'}",
        "income": lambda v: f"₹{int(v/1000)}K - ₹{int(v/1000) + 100}K (Approx.)",
    }

    mask_fn = masks.get(field_type, lambda v: "***MASKED***")
    return mask_fn(value)


def filter_response_by_privacy(data: dict, user: User, privacy_level: str = "PUBLIC") -> dict:
    """Filter response fields based on user's privacy access level"""
    if check_privacy_access(user, privacy_level):
        return data

    # Remove sensitive fields if user lacks access
    sensitive_fields = ["aadhar_number", "contact_number", "annual_income", "ration_card_number"]

    filtered = {k: v for k, v in data.items() if k not in sensitive_fields}

    logger.info(
        f"Response filtered for user {user.username}: removed {len(data) - len(filtered)} sensitive fields"
    )

    return filtered


class PrivacyMiddleware:
    """Middleware to enforce privacy and access control across all endpoints"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Get request path for logging
        path = scope.get("path", "unknown")

        # Log request (without sensitive data)
        logger.debug(f"Request to {path} from {scope.get('client', ['unknown'])[0]}")

        await self.app(scope, receive, send)