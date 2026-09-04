from typing import Dict, Any, List
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..models.issue import IssuePriority

class PriorityAgent(BaseAgent):
    """
    Priority Scoring Agent
    Ranks issues based on severity, affected count, and domain criticality
    """

    def __init__(self):
        super().__init__("Priority Scoring Agent", "Priority")

    # Priority weights
    SEVERITY_WEIGHTS = {
        "critical": 100,
        "high": 70,
        "medium": 40,
        "low": 10
    }

    DOMAIN_WEIGHTS = {
        "Health": 1.3,
        "Water": 1.3,
        "Education": 1.2,
        "Sanitation": 1.2,
        "Agriculture": 1.0,
        "Infrastructure": 1.0,
        "Electricity": 0.9
    }

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Context should contain agent_results from all domain agents
        """
        agent_results = context.get("agent_results", [])

        scored_issues = []

        for result in agent_results:
            domain = result.get("domain", "Unknown")
            severity = result.get("severity", "low")
            affected_count = result.get("affected_count", 0)
            issues_found = result.get("issues_found", [])

            # Calculate priority score
            base_score = self.SEVERITY_WEIGHTS.get(severity, 10)
            domain_multiplier = self.DOMAIN_WEIGHTS.get(domain, 1.0)
            affected_multiplier = min(1 + (affected_count / 100), 3.0)  # Cap at 3x

            priority_score = base_score * domain_multiplier * affected_multiplier

            scored_issues.append({
                "domain": domain,
                "severity": severity,
                "affected_count": affected_count,
                "priority_score": round(priority_score, 2),
                "issues_count": len(issues_found),
                "agent_name": result.get("agent_name")
            })

        # Sort by priority score
        scored_issues.sort(key=lambda x: x["priority_score"], reverse=True)

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "scored_issues": scored_issues,
            "top_priority_domain": scored_issues[0]["domain"] if scored_issues else None,
            "evidence": {
                "scoring_methodology": "severity × domain_weight × affected_multiplier",
                "total_issues_analyzed": len(scored_issues)
            }
        }

    def get_priority_recommendations(self, scored_issues: List[Dict]) -> List[str]:
        """Generate action recommendations based on priority scores"""
        if not scored_issues:
            return ["No critical issues identified"]

        top_3 = scored_issues[:3]
        recommendations = []

        for issue in top_3:
            recommendations.append(
                f"Address {issue['domain']} issues first (Priority Score: {issue['priority_score']}, "
                f"Severity: {issue['severity']}, {issue['affected_count']} affected)"
            )

        return recommendations
