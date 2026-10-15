from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.family_member import FamilyMember, EducationLevel
from ..models.issue import Issue, IssueCategory

class EducationAgent(BaseAgent):
    """Analyzes education-related indicators and issues"""

    # Domain constants
    HIGH_DROPOUT_THRESHOLD = 20
    MEDIUM_DROPOUT_THRESHOLD = 10
    HIGH_ILLITERACY_THRESHOLD = 30
    EDUCATION_SCHEMES = ["Samagra Shiksha", "Sarva Shiksha Abhiyan", "Rashtriya Madhyamik Shiksha"]

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
            if dropout_rate > self.HIGH_DROPOUT_THRESHOLD:
                severity = "high"
                issues_found.append({
                    "issue": "High school dropout or non-enrollment rate",
                    "description": f"{dropout_rate:.1f}% of school-age children not enrolled",
                    "impact": "Long-term development impact"
                })
            elif dropout_rate > self.MEDIUM_DROPOUT_THRESHOLD:
                severity = "medium"
                issues_found.append({
                    "issue": "Moderate education enrollment concern",
                    "description": f"{dropout_rate:.1f}% of school-age children not enrolled",
                    "impact": "Requires intervention"
                })

        # Check adult literacy
        illiteracy_rate = (illiterate_adults / total_adults) * 100 if total_adults > 0 else 0
        if illiteracy_rate > self.HIGH_ILLITERACY_THRESHOLD:
            severity = "medium" if severity == "low" else severity
            issues_found.append({
                "issue": "High adult illiteracy rate",
                "description": f"{illiteracy_rate:.1f}% of adults are illiterate",
                "impact": "Limits economic opportunities"
            })

        # Confidence calculation
        confidence_score = self.calculate_confidence(
            data_points=school_age_children + illiterate_adults,
            completeness=min((school_age_children + total_adults) / 500, 1.0)
        )

        # Trend analysis
        trend_data = self.get_trend_data(db, "education", days=30)

        # Match schemes to recommendations
        schemes_db = context.get("schemes_db", [])
        recommendations = []
        recommendations_with_schemes: List[Dict] = []

        if severity in ["medium", "high"]:
            recs_with_schemes = [
                {
                    "recommendation": "Launch adult literacy programs",
                    "suggested_schemes": self._match_schemes(schemes_db, ["adult literacy", "education"]),
                    "estimated_cost": "₹500-₹2000 per participant",
                    "timeline": "3-6 months"
                },
                {
                    "recommendation": "Implement mid-day meal schemes to improve enrollment",
                    "suggested_schemes": self._match_schemes(schemes_db, ["mid day meal", "nutrition"]),
                    "estimated_cost": "₹10-₹25 per child per day",
                    "timeline": "1-3 months"
                },
                {
                    "recommendation": "Provide scholarships for underprivileged children",
                    "suggested_schemes": self._match_schemes(schemes_db, ["scholarship", "stipend"]),
                    "estimated_cost": "Varies by scheme",
                    "timeline": "Ongoing"
                }
            ]
            recommendations_with_schemes = recs_with_schemes
            recommendations = [r["recommendation"] for r in recs_with_schemes]

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
            "recommendations": recommendations,
            "recommendations_with_schemes": recommendations_with_schemes,
            "confidence_score": round(confidence_score, 3),
            "trend_analysis": trend_data
        }

    def _match_schemes(self, schemes_db: List[Dict], keywords: List[str]) -> List[Dict]:
        """Match schemes based on keywords"""
        matched = []
        for scheme in schemes_db:
            scheme_text = " ".join([
                scheme.get("name", ""),
                scheme.get("description", ""),
                scheme.get("eligibility_criteria", ""),
                scheme.get("benefits", ""),
            ]).lower()

            score = sum(1 for kw in keywords if kw.lower() in scheme_text) / len(keywords) if keywords else 0
            if score > 0:
                matched.append({
                    "scheme_id": scheme.get("scheme_id"),
                    "name": scheme.get("name"),
                    "relevance_score": round(score, 2),
                })
        matched.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matched[:2]
