from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory

class InfrastructureAgent(BaseAgent):
    """Analyzes infrastructure issues - roads, electricity, etc."""

    def __init__(self):
        super().__init__("Infrastructure Agent", "Infrastructure")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        # Count infrastructure issues
        road_issues = db.query(Issue).filter(Issue.category == IssueCategory.ROAD).all()
        electricity_issues = db.query(Issue).filter(Issue.category == IssueCategory.ELECTRICITY).all()

        total_infra_issues = len(road_issues) + len(electricity_issues)

        issues_found = []
        severity = "low"

        if total_infra_issues > 15:
            severity = "high"
            issues_found.append({
                "issue": "Multiple infrastructure problems",
                "description": f"{total_infra_issues} infrastructure issues reported",
                "impact": "Affects daily life and economic activities"
            })
        elif total_infra_issues > 8:
            severity = "medium"
            issues_found.append({
                "issue": "Infrastructure needs attention",
                "description": f"{total_infra_issues} infrastructure issues pending",
                "impact": "May worsen if not addressed"
            })

        recommendations = []
        if severity in ["medium", "high"]:
            recommendations.extend([
                "Prioritize road repairs in most affected wards",
                "Apply for PMGSY (Pradhan Mantri Gram Sadak Yojana)",
                "Request electricity infrastructure upgrades",
                "Create ward-wise infrastructure maintenance plan"
            ])

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
            "recommendations": recommendations
        }
