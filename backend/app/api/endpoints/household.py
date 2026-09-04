from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...api.schemas import (
    HouseholdCreate, HouseholdResponse, HouseholdUpdate,
    FamilyMemberCreate, FamilyMemberResponse,
    IssueCreate, IssueResponse
)
from ...services.household_service import HouseholdService
from ...services.issue_service import IssueService

router = APIRouter()

@router.post("/register", response_model=HouseholdResponse, status_code=status.HTTP_201_CREATED)
def register_household(household_in: HouseholdCreate, db: Session = Depends(get_db)):
    """Register a new household (Family Head Portal)"""
    return HouseholdService.create_household(db, household_in)

@router.get("/{household_id}", response_model=HouseholdResponse)
def get_household(household_id: int, db: Session = Depends(get_db)):
    """Get household details by database ID"""
    return HouseholdService.get_household_by_id(db, household_id)

@router.get("/code/{hh_code}", response_model=HouseholdResponse)
def get_household_by_code(hh_code: str, db: Session = Depends(get_db)):
    """Get household details by unique Household ID (e.g. HH-W1-ABCD12)"""
    return HouseholdService.get_household_by_hh_id(db, hh_code)

@router.post("/{household_id}/members", response_model=FamilyMemberResponse, status_code=status.HTTP_201_CREATED)
def add_family_member(household_id: int, member_in: FamilyMemberCreate, db: Session = Depends(get_db)):
    """Add a family member to the household (Auto-calculates population)"""
    return HouseholdService.add_family_member(db, household_id, member_in)

@router.get("/{household_id}/members", response_model=List[FamilyMemberResponse])
def get_family_members(household_id: int, db: Session = Depends(get_db)):
    """List all family members of a household"""
    return HouseholdService.list_household_members(db, household_id)

@router.post("/{household_id}/issues", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def report_issue(household_id: int, issue_in: IssueCreate, db: Session = Depends(get_db)):
    """Report a village / service problem from household"""
    return IssueService.create_issue(db, household_id, issue_in)
