from abc import ABC, abstractmethod
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime

class BaseAgent(ABC):
    """
    Base class for all specialized domain agents
    Each agent analyzes a specific development domain

    Enhanced with confidence scoring and trend analysis
    """

    def __init__(self, name: str, domain: str):
        self.name = name
        self.domain = domain

    @abstractmethod
    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data and return structured findings
        Returns:
        {
            "agent_name": str,
            "domain": str,
            "issues_found": List[Dict],
            "severity": str,  # "low", "medium", "high", "critical"
            "affected_count": int,
            "evidence": Dict,
            "recommendations": List[str],
            "confidence_score": float,  # 0.0 - 1.0
            "trend_analysis": Dict,
            "recommendations_with_schemes": List[Dict],
        }
        """
        pass

    def generate_evidence(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured evidence for explainability"""
        return {
            "agent": self.name,
            "domain": self.domain,
            "findings": findings,
            "timestamp": str(self._get_timestamp())
        }

    def calculate_confidence(self, data_points: int, completeness: float = 1.0) -> float:
        """
        Calculate confidence score for agent analysis
        Based on data volume, completeness, and recent activity
        """
        # Base confidence starts at 0.5
        base = 0.5

        # More data points = higher confidence
        if data_points > 50:
            base += 0.3
        elif data_points > 20:
            base += 0.2
        elif data_points > 5:
            base += 0.1

        # Data completeness factor
        base += 0.2 * completeness

        return min(base, 1.0)

    def get_trend_data(self, db: Session, category: str, days: int = 30) -> Dict[str, Any]:
        """
        Get trend data for a specific issue category over time
        """
        from sqlalchemy import func, text
        from ..models.issue import Issue, IssueCategory

        # Map category string to enum
        category_map = {
            "water": IssueCategory.WATER,
            "sanitation": IssueCategory.SANITATION,
            "road": IssueCategory.ROAD,
            "health": IssueCategory.HEALTH,
            "education": IssueCategory.EDUCATION,
            "agriculture": IssueCategory.AGRICULTURE,
            "electricity": IssueCategory.ELECTRICITY,
        }

        cat_enum = category_map.get(category.lower())

        # Get count of issues created in recent time
        recent_cutoff = text(f"datetime('now', '-{days} days')")

        issue_count = db.query(func.count(Issue.id)).filter(
            Issue.category == cat_enum,
            Issue.created_at >= func.datetime('now', f'-{days} days')
        ).scalar() or 0

        return {
            "period_days": days,
            "new_issues_in_period": issue_count,
            "average_per_week": round(issue_count / (days / 7), 2) if days > 0 else 0
        }

    def match_schemes_for_issue(self, context: Dict[str, Any], issue_description: str) -> List[Dict]:
        """
        Match government schemes to an issue using keyword matching
        Returns list of matched schemes with relevance scores
        """
        schemes_db = context.get("schemes_db", [])
        if not schemes_db:
            return []

        matched = []
        keywords = issue_description.lower().split()

        for scheme in schemes_db:
            # Calculate relevance score based on keyword overlap
            scheme_text = " ".join([
                scheme.get("name", "").lower(),
                scheme.get("description", "").lower(),
                scheme.get("eligibility_criteria", "").lower(),
                scheme.get("benefits", "").lower(),
            ])

            # Simple keyword matching
            score = 0
            for kw in keywords:
                if len(kw) > 3 and kw in scheme_text:
                    score += 1

            if score > 0:
                matched.append({
                    "scheme_id": scheme.get("scheme_id"),
                    "name": scheme.get("name"),
                    "level": scheme.get("level"),
                    "category": scheme.get("category"),
                    "relevance_score": round(score / len(keywords), 2) if keywords else 0,
                    "link": scheme.get("official_link")
                })

        # Sort by relevance and return top 3
        matched.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matched[:3]

    def _get_timestamp(self):
        return datetime.utcnow()
