from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# Enums
class UserRole(str, Enum):
    FAMILY_HEAD = "Family Head"
    SARPANCH = "Sarpanch"
    PANCHAYAT_ADMIN = "Panchayat Admin"
    SYSTEM_ADMIN = "System Admin"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class EducationLevel(str, Enum):
    ILLITERATE = "Illiterate"
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    HIGHER_SECONDARY = "Higher Secondary"
    GRADUATE = "Graduate"
    POSTGRADUATE = "Postgraduate"

class IssueCategory(str, Enum):
    WATER = "Water"
    SANITATION = "Sanitation"
    ROAD = "Road & Infrastructure"
    HEALTH = "Health"
    EDUCATION = "Education"
    AGRICULTURE = "Agriculture"
    ELECTRICITY = "Electricity"
    OTHER = "Other"

class IssueStatus(str, Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"

class HouseholdType(str, Enum):
    APL = "APL"
    BPL = "BPL"
    ANTODAYA = "Antodaya"

# User & Auth Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.FAMILY_HEAD
    phone_number: Optional[str] = None
    preferred_language: str = "mr"

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class AuditLogResponse(BaseModel):
    id: int
    actor_id: int
    actor_role: Optional[str]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[dict]
    timestamp: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    phone_number: Optional[str] = None
    preferred_language: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Household Schemas
class HouseholdCreate(BaseModel):
    head_name: str = Field(..., min_length=2, max_length=200)
    head_age: int = Field(..., ge=18, le=120)
    head_gender: str
    head_occupation: Optional[str] = None
    contact_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    address: str
    ward_id: int
    household_type: HouseholdType = HouseholdType.APL
    annual_income: Optional[float] = None
    ration_card_number: Optional[str] = None

class HouseholdUpdate(BaseModel):
    head_name: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    annual_income: Optional[float] = None

class HouseholdResponse(BaseModel):
    id: int
    household_id: str
    head_name: str
    head_age: int
    head_gender: str
    contact_number: str
    address: str
    ward_id: int
    household_type: HouseholdType
    total_members: int
    created_at: datetime

    class Config:
        from_attributes = True

# Family Member Schemas
class FamilyMemberCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=200)
    age: int = Field(..., ge=0, le=120)
    gender: Gender
    relation_to_head: str
    date_of_birth: Optional[date] = None
    aadhar_number: Optional[str] = Field(None, pattern=r"^\d{12}$")
    education_level: Optional[EducationLevel] = None
    occupation: Optional[str] = None
    is_employed: bool = False
    is_student: bool = False
    has_health_issues: bool = False
    health_issue_description: Optional[str] = None

class FamilyMemberResponse(BaseModel):
    id: int
    household_id: int
    full_name: str
    age: int
    gender: Gender
    relation_to_head: str
    education_level: Optional[EducationLevel]
    occupation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Issue Schemas
class IssueCreate(BaseModel):
    category: IssueCategory
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    affected_count: int = Field(default=1, ge=1)
    language: str = "en"

class IssueResponse(BaseModel):
    id: int
    issue_id: str
    household_id: int
    category: IssueCategory
    title: str
    description: str
    status: IssueStatus
    priority: str
    affected_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# AI Recommendation Schemas
class RecommendationResponse(BaseModel):
    id: int
    recommendation_id: str
    issue_id: int
    priority_score: float
    recommendation_text: str
    evidence: dict
    affected_wards: List[int]
    affected_households: int
    suggested_schemes: List[int]
    estimated_cost: Optional[float]
    estimated_timeline: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Ward Schemas
class WardResponse(BaseModel):
    id: int
    ward_number: int
    ward_name: str
    population: int
    total_households: int

    class Config:
        from_attributes = True

# Analytics Schemas
class PopulationAnalytics(BaseModel):
    total_population: int
    total_households: int
    male_population: int
    female_population: int
    children: int
    adults: int
    senior_citizens: int
    avg_household_size: float
    literacy_rate: float
    employment_rate: float

class WardAnalytics(BaseModel):
    ward_id: int
    ward_name: str
    population: int
    households: int
    issues_count: int
    high_priority_issues: int

class DomainAnalytics(BaseModel):
    domain: str
    total_issues: int
    resolved_issues: int
    pending_issues: int
    critical_issues: int
    avg_resolution_time: Optional[float]

# Scheme Schemas
class SchemeResponse(BaseModel):
    id: int
    scheme_id: str
    name: str
    category: str
    level: str
    description: str
    eligibility_criteria: Optional[str]
    benefits: Optional[str]
    official_link: Optional[str]

    class Config:
        from_attributes = True
