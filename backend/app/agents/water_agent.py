from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory, IssuePriority
from ..models.household import Household

class WaterAgent(BaseAgent):
    """Analyzes water and sanitation issues"""

    # Domain constants
    CRITICAL_THRESHOLD = 30
    HIGH_THRESHOLD = 15
    HIGH_PRIORITY_LIMIT = 5
    WATER_SCHEMES = ["Jal Jeevan Mission", "Swachh Bharat Mission", "Atal Jyoti"]

    def __init__(self):
        super().__init__("Water & Sanitation Agent", "Water")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        # Count water-related issues
        water_issues = db.query(Issue).filter(Issue.category == IssueCategory.WATER).all()
        sanitation_issues = db.query(Issue).filter(Issue.category == IssueCategory.SANITATION).all()

        total_issues = len(water_issues) + len(sanitation_issues)
        total_households = db.query(func.count(Household.id)).scalar() or 1

        issues_found = []
        severity = "low"
        affected_count = sum(issue.affected_count for issue in water_issues + sanitation_issues)

        # Calculate percentage affected
        pct_affected = (affected_count / total_households) * 100 if total_households > 0 else 0

        if pct_affected > self.CRITICAL_THRESHOLD:
            severity = "high"
            issues_found.append({
                "issue": "High percentage of households reporting water issues",
                "description": f"{pct_affected:.1f}% households affected by water/sanitation problems",
                "impact": "Health and quality of life concerns"
            })
        elif pct_affected > self.HIGH_THRESHOLD:
            severity = "medium"
            issues_found.append({
                "issue": "Moderate water/sanitation concerns",
                "description": f"{pct_affected:.1f}% households affected",
                "impact": "Requires attention"
            })

        # Check for high-priority unresolved issues
        high_priority_count = len([i for i in water_issues + sanitation_issues
                                     if i.priority in [IssuePriority.HIGH, IssuePriority.CRITICAL]
                                     and i.status.value in ["Submitted", "Under Review"]])

        if high_priority_count > self.HIGH_PRIORITY_LIMIT:
            severity = "critical"
            issues_found.append({
                "issue": f"{high_priority_count} high-priority water issues pending",
                "description": "Multiple urgent water/sanitation issues require immediate attention",
                "impact": "Public health risk"
            })

        # Confidence calculation
        confidence_score = self.calculate_confidence(
            data_points=len(water_issues) + len(sanitation_issues),
            completeness=min(total_households / 100, 1.0)
        )

        # Trend analysis
        trend_data = self.get_trend_data(db, "water", days=30)

        # Match schemes to recommendations
        schemes_db = context.get("schemes_db", [])
        recommendations = []
        recommendations_with_schemes: List[Dict] = []

        if severity in ["high", "critical"]:
            recs_with_schemes = [
                {
                    "recommendation": "Conduct immediate water quality assessment",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Jal Jeevan", "water quality"]),
                    "estimated_cost": "₹50,000 - ₹1,00,000",
                    "timeline": "2-4 weeks"
                },
                {
                    "recommendation": "Allocate emergency funds for water infrastructure repair",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Jal Jeevan Mission"]),
                    "estimated_cost": "₹2,00,000+",
                    "timeline": "1-3 months"
                },
                {
                    "recommendation": "Consider applying for Jal Jeevan Mission scheme",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Jal Jeevan Mission"]),
                    "estimated_cost": "Subsidized/Grant",
                    "timeline": "3-6 months"
                }
            ]
            recommendations_with_schemes = recs_with_schemes
            recommendations = [r["recommendation"] for r in recs_with_schemes]

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "issues_found": issues_found,
            "severity": severity,
            "affected_count": affected_count,
            "evidence": {
                "water_issues_count": len(water_issues),
                "sanitation_issues_count": len(sanitation_issues),
                "percentage_affected": round(pct_affected, 2),
                "high_priority_pending": high_priority_count
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

            score = sum(1 for kw in keywords if kw.lower() in scheme_text) / len(keywords)
            if score > 0:
                matched.append({
                    "scheme_id": scheme.get("scheme_id"),
                    "name": scheme.get("name"),
                    "relevance_score": round(score, 2),
                })
        matched.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matched[:2]
