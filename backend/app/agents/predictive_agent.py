from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.issue import Issue, IssueCategory, IssueStatus
from ..models.household import Household

class PredictiveAnalyticsAgent(BaseAgent):
    """
    Predictive Analytics Agent
    Forecasts future village issues based on historical trends, seasonal patterns,
    and demographic projections for proactive decision-making.
    Enhanced with trend forecasting and risk prediction.
    """

    # Risk thresholds
    HIGH_RISK_THRESHOLD = 0.75  # 75% probability of escalation
    MEDIUM_RISK_THRESHOLD = 0.40  # 40% probability
    FORECAST_DAYS = 90  # 3-month forecast window

    def __init__(self):
        super().__init__("Predictive Analytics Agent", "Predictive")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run predictive analysis on village data"""
        # Get all unresolved issues
        unresolved_issues = db.query(Issue).filter(
            Issue.status.in_([IssueStatus.SUBMITTED, IssueStatus.UNDER_REVIEW, IssueStatus.IN_PROGRESS])
        ).all()

        # Total households for risk calculation
        total_households = db.query(func.count(Household.id)).scalar() or 1

        # Calculate escalation risk per domain
        domain_risks = self._calculate_domain_risks(db, unresolved_issues)

        # Predict future issue trends
        trend_forecasts = self._forecast_trends(db)

        # Generate predictive recommendations
        predictions = []
        predictions_with_schemes = []

        for domain, risk_score in domain_risks.items():
            if risk_score > self.HIGH_RISK_THRESHOLD:
                predictions.append({
                    "domain": domain,
                    "prediction": f"Critical escalation risk in {domain}",
                    "probability": round(risk_score, 2),
                    "action": "Immediate preventive action recommended"
                })
                predictions_with_schemes.append({
                    "prediction_text": f"Prepare for critical escalation in {domain} domain",
                    "domain": domain,
                    "risk_score": round(risk_score, 2),
                    "suggested_schemes": self._get_preventive_schemes(context.get("schemes_db", []), domain),
                    "recommended_timeline": "Within 2 weeks"
                })
            elif risk_score > self.MEDIUM_RISK_THRESHOLD:
                predictions.append({
                    "domain": domain,
                    "prediction": f"Moderate escalation risk in {domain}",
                    "probability": round(risk_score, 2),
                    "action": "Monitor closely and plan preventive measures"
                })
                predictions_with_schemes.append({
                    "prediction_text": f"Monitor escalation risk in {domain} domain",
                    "domain": domain,
                    "risk_score": round(risk_score, 2),
                    "suggested_schemes": self._get_preventive_schemes(context.get("schemes_db", []), domain),
                    "recommended_timeline": "Within 1 month"
                })

        # Overall confidence
        confidence_score = self.calculate_confidence(
            data_points=len(unresolved_issues),
            completeness=min(len(unresolved_issues) / 10, 1.0)
        )

        return {
            "agent_name": self.name,
            "domain": self.domain,
            "issues_found": predictions,
            "severity": "high" if any(p.get("probability", 0) > self.HIGH_RISK_THRESHOLD for p in predictions) else ("medium" if predictions else "low"),
            "affected_count": len(unresolved_issues),
            "evidence": {
                "unresolved_issues_count": len(unresolved_issues),
                "forecast_window_days": self.FORECAST_DAYS,
                "trend_forecasts": trend_forecasts,
            },
            "recommendations": [
                "Implement predictive monitoring for high-risk domains",
                "Establish early warning system for issue escalation",
                "Create contingency plans for critical predictions"
            ],
            "recommendations_with_schemes": predictions_with_schemes,
            "confidence_score": round(confidence_score, 3),
            "trend_analysis": {
                "forecast_period": f"{self.FORECAST_DAYS} days",
                "total_predictions": len(predictions)
            },
            "predictions": predictions,
            "domain_risks": domain_risks
        }

    def _calculate_domain_risks(self, db: Session, issues: List) -> Dict[str, float]:
        """Calculate risk scores per domain based on unresolved issues"""
        from collections import Counter
        from ..models.issue import IssueCategory

        domain_counts = Counter(i.category.value for i in issues)
        priorities = Counter(i.priority.value for i in issues)

        # Count critical/high unresolved
        critical_unresolved = len([i for i in issues if i.priority.value == "Critical"])
        high_unresolved = len([i for i in issues if i.priority.value == "High"])
        total_unresolved = len(issues)

        # Calculate risk per domain
        risks = {}
        for domain, count in domain_counts.items():
            # Risk formula: (critical * 0.5) + (high * 0.3) + (count/total)
            critical_in_domain = len([
                i for i in issues
                if i.category.value == domain and i.priority.value == "Critical"
            ])
            high_in_domain = len([
                i for i in issues
                if i.category.value == domain and i.priority.value == "High"
            ])

            risk_score = (critical_in_domain * 0.5 + high_in_domain * 0.3) / max(count, 1)
            # Add base risk based on issue volume
            risk_score += min(count / max(total_unresolved, 1), 0.5)

            # Cap at 1.0
            risks[domain] = min(risk_score, 1.0)

        return risks

    def _forecast_trends(self, db: Session) -> Dict[str, Any]:
        """Forecast trends based on recent issue patterns"""
        from sqlalchemy import func, and_
        from datetime import datetime, timedelta
        from ..models.issue import Issue

        # Recent issues (last 30 days)
        recent_cutoff = datetime.utcnow() - timedelta(days=30)
        recent_issues = db.query(Issue).filter(Issue.created_at >= recent_cutoff).count()

        # Previous period issues (30-60 days ago)
        prev_start = datetime.utcnow() - timedelta(days=60)
        prev_end = datetime.utcnow() - timedelta(days=30)
        previous_issues = db.query(Issue).filter(
            Issue.created_at >= prev_start,
            Issue.created_at < prev_end
        ).count()

        # Trend: increasing, stable, or decreasing
        trend = "stable"
        if previous_issues > 0:
            change_ratio = recent_issues / previous_issues
            if change_ratio > 1.3:
                trend = "increasing"
            elif change_ratio < 0.7:
                trend = "decreasing"

        # Project future volume
        projected_issues = int(recent_issues * (1 + (recent_issues - previous_issues) / max(previous_issues, 1)))

        return {
            "recent_issues_30_days": recent_issues,
            "previous_issues_30_60_days": previous_issues,
            "trend_direction": trend,
            "projected_issues_30_days": max(projected_issues, recent_issues),  # Never below current
            "change_percentage": round(
                ((recent_issues - previous_issues) / max(previous_issues, 1)) * 100, 1
            )
        }

    def _get_preventive_schemes(self, schemes_db: List[Dict], domain: str) -> List[Dict]:
        """Get preventive schemes for a domain"""
        matched = []
        domain_keywords = {
            "Water": ["water", "sanitation", "Jal Jeevan"],
            "Health": ["health", "Ayushman", "medical"],
            "Education": ["education", "school", "scholarship"],
            "Infrastructure": ["road", "PMGSY", "infrastructure"],
            "Agriculture": ["agriculture", "PM-KISAN", "farmer"],
        }.get(domain, [])

        for scheme in schemes_db:
            scheme_text = " ".join([
                scheme.get("name", ""),
                scheme.get("description", ""),
                scheme.get("category", ""),
            ]).lower()

            score = sum(1 for kw in domain_keywords if kw.lower() in scheme_text) / len(domain_keywords) if domain_keywords else 0
            if score > 0:
                matched.append({
                    "scheme_id": scheme.get("scheme_id"),
                    "name": scheme.get("name"),
                    "relevance_score": round(score, 2),
                    "level": scheme.get("level"),
                    "category": scheme.get("category"),
                })

        matched.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return matched[:2]