import uuid
from sqlalchemy.orm import Session
from ..models.household import Household
from ..models.family_member import FamilyMember
from ..models.ward import Ward
from ..api.schemas import HouseholdCreate, HouseholdUpdate, FamilyMemberCreate
from fastapi import HTTPException, status

class HouseholdService:
    @staticmethod
    def generate_household_id(ward_number: int) -> str:
        return f"HH-W{ward_number}-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def create_household(db: Session, household_in: HouseholdCreate) -> Household:
        # Verify ward exists
        ward = db.query(Ward).filter(Ward.id == household_in.ward_id).first()
        if not ward:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ward with id {household_in.ward_id} not found"
            )

        # Generate unique Household ID
        hh_id = HouseholdService.generate_household_id(ward.ward_number)

        db_household = Household(
            household_id=hh_id,
            head_name=household_in.head_name,
            head_age=household_in.head_age,
            head_gender=household_in.head_gender,
            head_occupation=household_in.head_occupation,
            contact_number=household_in.contact_number,
            address=household_in.address,
            ward_id=household_in.ward_id,
            household_type=household_in.household_type,
            annual_income=household_in.annual_income,
            ration_card_number=household_in.ration_card_number,
            total_members=1 # Head counts as 1 initially
        )

        db.add(db_household)
        db.flush() # Flush to get db_household.id

        # Also add head of family as the first family member
        head_member = FamilyMember(
            household_id=db_household.id,
            full_name=household_in.head_name,
            age=household_in.head_age,
            gender=household_in.head_gender,
            relation_to_head="Self (Head)",
            occupation=household_in.head_occupation,
            is_employed=True if household_in.head_occupation else False
        )
        db.add(head_member)

        # Update ward totals
        ward.total_households += 1
        ward.population += 1

        db.commit()
        db.refresh(db_household)
        return db_household

    @staticmethod
    def add_family_member(db: Session, household_id: int, member_in: FamilyMemberCreate) -> FamilyMember:
        household = db.query(Household).filter(Household.id == household_id).first()
        if not household:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Household with id {household_id} not found"
            )

        # Check duplicate aadhar if provided
        if member_in.aadhar_number:
            existing = db.query(FamilyMember).filter(FamilyMember.aadhar_number == member_in.aadhar_number).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Aadhar number already registered in another household"
                )

        member = FamilyMember(
            household_id=household_id,
            full_name=member_in.full_name,
            age=member_in.age,
            gender=member_in.gender,
            relation_to_head=member_in.relation_to_head,
            date_of_birth=member_in.date_of_birth,
            aadhar_number=member_in.aadhar_number,
            education_level=member_in.education_level,
            occupation=member_in.occupation,
            is_employed=member_in.is_employed,
            is_student=member_in.is_student,
            has_health_issues=member_in.has_health_issues,
            health_issue_description=member_in.health_issue_description
        )

        db.add(member)

        # Increment household count & ward population automatically
        household.total_members += 1
        if household.ward:
            household.ward.population += 1

        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def get_household_by_id(db: Session, household_id: int) -> Household:
        household = db.query(Household).filter(Household.id == household_id).first()
        if not household:
            raise HTTPException(status_code=404, detail="Household not found")
        return household

    @staticmethod
    def get_household_by_hh_id(db: Session, hh_id: str) -> Household:
        household = db.query(Household).filter(Household.household_id == hh_id).first()
        if not household:
            raise HTTPException(status_code=404, detail="Household not found")
        return household

    @staticmethod
    def list_household_members(db: Session, household_id: int):
        return db.query(FamilyMember).filter(FamilyMember.household_id == household_id).all()
