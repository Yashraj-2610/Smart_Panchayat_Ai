from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory
from ..models.family_member import FamilyMember

class HealthAgent(BaseAgent):
    """Analyzes health-related indicators and issues"""

    # Domain constants
    CRITICAL_THRESHOLD = 25
    HIGH_THRESHOLD = 15
    MEDIUM_THRESHOLD = 8
    SANITATION_RISK_THRESHOLD = 10
    HEALTH_SCHEMES = ["Ayushman Bharat", "National Health Mission", "Pradhan Mantri Matru Vandana"]

    def __init__(self):
        super().__init__("Health Agent", "Health")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        # Count health issues
        health_issues = db.query(Issue).filter(Issue.category == IssueCategory.HEALTH).all()

        # Count people with reported health issues
        members_with_health_issues = db.query(func.count(FamilyMember.id)).filter(
            FamilyMember.has_health_issues == True
        ).scalar() or 0

        total_population = db.query(func.count(FamilyMember.id)).scalar() or 1

        issues_found = []
        severity = "low"

        health_issue_rate = (members_with_health_issues / total_population) * 100 if total_population > 0 else 0

        if health_issue_rate > self.CRITICAL_THRESHOLD:
            severity = "high"
            issues_found.append({
                "issue": "High prevalence of health issues",
                "description": f"{health_issue_rate:.1f}% of population reporting health concerns",
                "impact": "Public health intervention needed"
            })
        elif health_issue_rate > self.HIGH_THRESHOLD:
            severity = "medium"
            issues_found.append({
                "issue": "Moderate health concerns",
                "description": f"{health_issue_rate:.1f}% of population with health issues",
                "impact": "Healthcare access may be inadequate"
            })

        # Check for sanitation-related health risks
        sanitation_issues = db.query(func.count(Issue.id)).filter(
            Issue.category == IssueCategory.SANITATION
        ).scalar() or 0

        if sanitation_issues > self.SANITATION_RISK_THRESHOLD:
            severity = "high" if severity != "critical" else severity
            issues_found.append({
                "issue": "Sanitation affecting health",
                "description": f"{sanitation_issues} sanitation issues may create health risks",
                "impact": "Disease outbreak risk"
            })

        # Confidence calculation
        confidence_score = self.calculate_confidence(
            data_points=len(health_issues) + members_with_health_issues,
            completeness=min(total_population / 1000, 1.0)
        )

        # Trend analysis
        trend_data = self.get_trend_data(db, "health", days=30)

        # Match schemes to recommendations
        schemes_db = context.get("schemes_db", [])
        recommendations = []
        recommendations_with_schemes: List[Dict] = []

        if severity in ["medium", "high", "critical"]:
            recs_with_schemes = [
                {
                    "recommendation": "Organize free health checkup camps",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Ayushman", "health camp"]),
                    "estimated_cost": "₹15,000 - ₹30,000 per camp",
                    "timeline": "1-2 weeks"
                },
                {
                    "recommendation": "Improve access to Primary Health Center (PHC)",
                    "suggested_schemes": self._match_schemes(schemes_db, ["National Health Mission", "PHC"]),
                    "estimated_cost": "₹1,00,000 - ₹5,00,000",
                    "timeline": "2-6 months"
                },
                {
                    "recommendation": "Apply for Ayushman Bharat and other health schemes",
                    "suggested_schemes": self._match_schemes(schemes_db, ["Ayushman Bharat"]),
                    "estimated_cost": "Government funded",
                    "timeline": "1-3 months"
                }
            ]
            recommendations_with_schemes = recs_with_schemes
            recommendations = [r["recommendation"] for r in recs_with_schemes]

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "issues_found": issues_found,
            "severity": severity,
            "affected_count": members_with_health_issues,
            "evidence": {
                "health_issues_reported": len(health_issues),
                "members_with_health_issues": members_with_health_issues,
                "health_issue_rate": round(health_issue_rate, 2),
                "sanitation_issues": sanitation_issues
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
