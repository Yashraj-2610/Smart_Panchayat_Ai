from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.family_member import FamilyMember, EducationLevel
from ..models.issue import Issue, IssueCategory

class EducationAgent(BaseAgent):
    """Analyzes education-related indicators and issues"""

    def __init__(self):
        super().__init__("Education Agent", "Education")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        # Count school-age children (5-18 years)
        school_age_children = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.age >= 5,
            FamilyMember.age <= 18
        ).scalar() or 0

        # Count students
        students = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.is_student == True
        ).scalar() or 0

        # Count illiterate adults (18+)
        illiterate_adults = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.age >= 18,
            FamilyMember.education_level == EducationLevel.ILLITERATE
        ).scalar() or 0

        total_adults = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.age >= 18
        ).scalar() or 1

        # Education issues
        education_issues = db.query(Issue).filter(Issue.category == IssueCategory.EDUCATION).all()

        issues_found = []
        severity = "low"

        # Calculate dropout/non-enrollment rate
        enrollment_gap = school_age_children - students
        if enrollment_gap > 0:
            dropout_rate = (enrollment_gap / school_age_children) * 100 if school_age_children > 0 else 0
            if dropout_rate > 20:
                severity = "high"
                issues_found.append({
                    "issue": "High school dropout or non-enrollment rate",
                    "description": f"{dropout_rate:.1f}% of school-age children not enrolled",
                    "impact": "Long-term development impact"
                })
            elif dropout_rate > 10:
                severity = "medium"
                issues_found.append({
                    "issue": "Moderate education enrollment concern",
                    "description": f"{dropout_rate:.1f}% of school-age children not enrolled",
                    "impact": "Requires intervention"
                })

        # Check adult literacy
        illiteracy_rate = (illiterate_adults / total_adults) * 100 if total_adults > 0 else 0
        if illiteracy_rate > 30:
            severity = "medium" if severity == "low" else severity
            issues_found.append({
                "issue": "High adult illiteracy rate",
                "description": f"{illiteracy_rate:.1f}% of adults are illiterate",
                "impact": "Limits economic opportunities"
            })

        recommendations = []
        if severity in ["medium", "high"]:
            recommendations.extend([
                "Launch adult literacy programs",
                "Implement mid-day meal schemes to improve enrollment",
                "Provide scholarships for underprivileged children",
                "Apply for Samagra Shiksha Abhiyan funds"
            ])

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "issues_found": issues_found,
            "severity": severity,
            "affected_count": enrollment_gap + illiterate_adults,
            "evidence": {
                "school_age_children": school_age_children,
                "enrolled_students": students,
                "enrollment_gap": enrollment_gap,
                "illiterate_adults": illiterate_adults,
                "illiteracy_rate": round(illiteracy_rate, 2),
                "education_issues_reported": len(education_issues)
            },
            "recommendations": recommendations
        }
