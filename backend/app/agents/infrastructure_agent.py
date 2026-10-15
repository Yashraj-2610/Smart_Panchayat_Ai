from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory

class InfrastructureAgent(BaseAgent):
    """Analyzes infrastructure issues - roads, electricity, etc."""

    # Domain constants
    HIGH_INFRA_THRESHOLD = 15
    MEDIUM_INFRA_THRESHOLD = 8
    INFRA_SCHEMES = ["PMGSY", "Saubhagya", "Deen Dayal Upadhyaya Gram Jyoti"]

    def __init__(self):
        super().__init__("Infrastructure Agent", "Infrastructure")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        # Count infrastructure issues
        road_issues = db.query(Issue).filter(Issue.category == IssueCategory.ROAD).all()
        electricity_issues = db.query(Issue).filter(Issue.category == IssueCategory.ELECTRICITY).all()

        total_infra_issues = len(road_issues) + len(electricity_issues)

        issues_found = []
        severity = "low"

        if total_infra_issues > self.HIGH_INFRA_THRESHOLD:
            severity = "high"
            issues_found.append({
                "issue": "Multiple infrastructure problems",
                "description": f"{total_infra_issues} infrastructure issues reported",
                "impact": "Affects daily life and economic activities"
            })
        elif total_infra_issues > self.MEDIUM_INFRA_THRESHOLD:
            severity = "medium"
            issues_found.append({
                "issue": "Infrastructure needs attention",
                "description": f"{total_infra_issues} infrastructure issues pending",
                "impact": "May worsen if not addressed"
            })

        # Confidence calculation
        confidence_score = self.calculate_confidence(
            data_points=total_infra_issues,
            completeness=1.0  # Issues are always tracked
        )

        # Trend analysis
        trend_data = self.get_trend_data(db, "road", days=30)

        # Match schemes to recommendations
        schemes_db = context.get("schemes_db", [])
        recommendations = []
        recommendations_with_schemes: List[Dict] = []

        if severity in ["medium", "high"]:
            recs_with_schemes = [
                {
                    "recommendation": "Prioritize road repairs in most affected wards",
                    "suggested_schemes": self._match_schemes(schemes_db, ["PMGSY", "road"]),
                    "estimated_cost": "₹5,00,000 - ₹50,00,000",
                    "timeline": "3-12 months"
                },
                {
                    "recommendation": "Apply for PMGSY (Pradhan Mantri Gram Sadak Yojana)",
                    "suggested_schemes": self._match_schemes(schemes_db, ["PMGSY", "connectivity"]),
                    "estimated_cost": "Central government funded",
                    "timeline": "6-24 months"
                },
                {
                    "recommendation": "Request electricity infrastructure upgrades",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Saubhagya", "electricity"]),
                    "estimated_cost": "Subsidized",
                    "timeline": "2-6 months"
                }
            ]
            recommendations_with_schemes = recs_with_schemes
            recommendations = [r["recommendation"] for r in recs_with_schemes]

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "issues_found": issues_found,
            "severity": severity,
            "affected_count": sum(i.affected_count for i in road_issues + electricity_issues),
            "evidence": {
                "road_issues": len(road_issues),
                "electricity_issues": len(electricity_issues),
                "total_infrastructure_issues": total_infra_issues
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
