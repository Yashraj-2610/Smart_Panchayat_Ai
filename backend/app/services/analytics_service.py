from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.household import Household, HouseholdType
from ..models.family_member import FamilyMember, Gender, EducationLevel
from ..models.ward import Ward
from ..models.issue import Issue, IssuePriority, IssueStatus
from typing import Dict, Any, List

class AnalyticsService:
    @staticmethod
    def get_population_summary(db: Session) -> Dict[str, Any]:
        total_households = db.query(func.count(Household.id)).scalar() or 0
        total_members = db.query(func.count(FamilyMember.id)).scalar() or 0

        # Gender breakdown
        male_count = db.query(func.count(FamilyMember.id)).filter(FamilyMember.gender == Gender.MALE).scalar() or 0
        female_count = db.query(func.count(FamilyMember.id)).filter(FamilyMember.gender == Gender.FEMALE).scalar() or 0
        other_count = db.query(func.count(FamilyMember.id)).filter(FamilyMember.gender == Gender.OTHER).scalar() or 0

        # Age group breakdown
        children = db.query(func.count(FamilyMember.id)).filter(FamilyMember.age < 18).scalar() or 0
        adults = db.query(func.count(FamilyMember.id)).filter(FamilyMember.age >= 18, FamilyMember.age < 60).scalar() or 0
        seniors = db.query(func.count(FamilyMember.id)).filter(FamilyMember.age >= 60).scalar() or 0

        # Literacy and Employment
        literate_count = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.education_level.isnot(None),
            FamilyMember.education_level != EducationLevel.ILLITERATE
        ).scalar() or 0

        employed_count = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.is_employed == True
        ).scalar() or 0

        # Poverty categories
        bpl_count = db.query(func.count(Household.id)).filter(Household.household_type == HouseholdType.BPL).scalar() or 0
        apl_count = db.query(func.count(Household.id)).filter(Household.household_type == HouseholdType.APL).scalar() or 0
        antodaya_count = db.query(func.count(Household.id)).filter(Household.household_type == HouseholdType.ANTODAYA).scalar() or 0

        avg_size = round(total_members / total_households, 2) if total_households > 0 else 0
        literacy_rate = round((literate_count / total_members) * 100, 2) if total_members > 0 else 0
        employment_rate = round((employed_count / (adults if adults > 0 else 1)) * 100, 2) if total_members > 0 else 0

        return {
            "total_households": total_households,
            "total_population": total_members,
            "male_population": male_count,
            "female_population": female_count,
            "other_population": other_count,
            "children": children,
            "adults": adults,
            "senior_citizens": seniors,
            "avg_household_size": avg_size,
            "literacy_rate": literacy_rate,
            "employment_rate": employment_rate,
            "bpl_households": bpl_count,
            "apl_households": apl_count,
            "antodaya_households": antodaya_count
        }

    @staticmethod
    def get_ward_wise_analytics(db: Session) -> List[Dict[str, Any]]:
        wards = db.query(Ward).all()
        result = []

        for ward in wards:
            # Count households
            hh_count = db.query(func.count(Household.id)).filter(Household.ward_id == ward.id).scalar() or 0

            # Count members
            pop_count = db.query(func.count(FamilyMember.id)).join(Household).filter(Household.ward_id == ward.id).scalar() or 0

            # Count issues
            issues_count = db.query(func.count(Issue.id)).join(Household).filter(Household.ward_id == ward.id).scalar() or 0

            # High priority issues
            high_prio = db.query(func.count(Issue.id)).join(Household).filter(
                Household.ward_id == ward.id,
                Issue.priority.in_([IssuePriority.HIGH, IssuePriority.CRITICAL])
            ).scalar() or 0

            result.append({
                "ward_id": ward.id,
                "ward_number": ward.ward_number,
                "ward_name": ward.ward_name,
                "households": hh_count,
                "population": pop_count,
                "issues_count": issues_count,
                "high_priority_issues": high_prio
            })

        return result

    @staticmethod
    def get_issue_statistics(db: Session) -> Dict[str, Any]:
        total_issues = db.query(func.count(Issue.id)).scalar() or 0
        resolved_issues = db.query(func.count(Issue.id)).filter(Issue.status == IssueStatus.RESOLVED).scalar() or 0
        in_progress = db.query(func.count(Issue.id)).filter(Issue.status == IssueStatus.IN_PROGRESS).scalar() or 0
        pending_issues = db.query(func.count(Issue.id)).filter(Issue.status == IssueStatus.SUBMITTED).scalar() or 0

        # Issues by category
        categories = db.query(Issue.category, func.count(Issue.id)).group_by(Issue.category).all()
        by_category = {cat.value: count for cat, count in categories}

        # Issues by priority
        priorities = db.query(Issue.priority, func.count(Issue.id)).group_by(Issue.priority).all()
        by_priority = {prio.value: count for prio, count in priorities}

        return {
            "total_issues": total_issues,
            "resolved_issues": resolved_issues,
            "in_progress_issues": in_progress,
            "pending_issues": pending_issues,
            "by_category": by_category,
            "by_priority": by_priority
        }
