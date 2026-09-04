from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory
from ..models.family_member import FamilyMember

class HealthAgent(BaseAgent):
    """Analyzes health-related indicators and issues"""

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

        if health_issue_rate > 15:
            severity = "high"
            issues_found.append({
                "issue": "High prevalence of health issues",
                "description": f"{health_issue_rate:.1f}% of population reporting health concerns",
                "impact": "Public health intervention needed"
            })
        elif health_issue_rate > 8:
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

        if sanitation_issues > 10:
            severity = "high" if severity != "critical" else severity
            issues_found.append({
                "issue": "Sanitation affecting health",
                "description": f"{sanitation_issues} sanitation issues may create health risks",
                "impact": "Disease outbreak risk"
            })

        recommendations = []
        if severity in ["medium", "high", "critical"]:
            recommendations.extend([
                "Organize free health checkup camps",
                "Improve access to Primary Health Center (PHC)",
                "Apply for Ayushman Bharat and other health schemes",
                "Focus on sanitation improvements"
            ])

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
            "recommendations": recommendations
        }
