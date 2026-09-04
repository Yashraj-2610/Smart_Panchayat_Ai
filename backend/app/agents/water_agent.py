from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory, IssuePriority
from ..models.household import Household

class WaterAgent(BaseAgent):
    """Analyzes water and sanitation issues"""

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

        if pct_affected > 30:
            severity = "high"
            issues_found.append({
                "issue": "High percentage of households reporting water issues",
                "description": f"{pct_affected:.1f}% households affected by water/sanitation problems",
                "impact": "Health and quality of life concerns"
            })
        elif pct_affected > 15:
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

        if high_priority_count > 5:
            severity = "critical"
            issues_found.append({
                "issue": f"{high_priority_count} high-priority water issues pending",
                "description": "Multiple urgent water/sanitation issues require immediate attention",
                "impact": "Public health risk"
            })

        recommendations = []
        if severity in ["high", "critical"]:
            recommendations.extend([
                "Conduct immediate water quality assessment",
                "Allocate emergency funds for water infrastructure repair",
                "Consider applying for Jal Jeevan Mission scheme"
            ])

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
            "recommendations": recommendations
        }
