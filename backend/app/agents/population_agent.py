from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.household import Household
from ..models.family_member import FamilyMember
from ..models.ward import Ward

class PopulationAgent(BaseAgent):
    """Analyzes population and demographic data"""

    # Domain constants
    LOW_COVERAGE_THRESHOLD = 0.5
    WARD_IMBALANCE_RATIO = 2.0

    def __init__(self):
        super().__init__("Population & Demography Agent", "Population")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        total_households = db.query(func.count(Household.id)).scalar() or 0
        total_population = db.query(func.count(FamilyMember.id)).scalar() or 0

        issues_found = []
        severity = "low"

        # Check for low registration coverage (example threshold)
        expected_population = context.get("expected_population", 8000)
        if total_population < expected_population * self.LOW_COVERAGE_THRESHOLD:
            issues_found.append({
                "issue": "Low household registration coverage",
                "description": f"Only {total_population} people registered out of expected {expected_population}",
                "impact": "Limited data for decision-making"
            })
            severity = "medium"

        # Check for ward-level imbalances
        wards = db.query(Ward).all()
        ward_populations = []
        for ward in wards:
            pop = db.query(func.count(FamilyMember.id)).join(Household).filter(
                Household.ward_id == ward.id
            ).scalar() or 0
            ward_populations.append(pop)

        if ward_populations and max(ward_populations) > self.WARD_IMBALANCE_RATIO * min(ward_populations):
            issues_found.append({
                "issue": "Significant population imbalance across wards",
                "description": "Some wards are much more populated than others",
                "impact": "Unequal resource distribution"
            })

        # Confidence calculation
        confidence_score = self.calculate_confidence(
            data_points=total_households + total_population,
            completeness=min(total_population / expected_population, 1.0) if expected_population > 0 else 0.5
        )

        # Trend analysis
        trend_data = self.get_trend_data(db, "population", days=30)

        # Match schemes to recommendations
        schemes_db = context.get("schemes_db", [])
        recommendations = []
        recommendations_with_schemes: List[Dict] = []

        if issues_found:
            recs_with_schemes = [
                {
                    "recommendation": "Increase household registration drives",
                    "suggested_schemes": self._match_schemes(schemes_db, ["registration", "census"]),
                    "estimated_cost": "₹10,000 - ₹50,000 per drive",
                    "timeline": "1-2 months"
                },
                {
                    "recommendation": "Focus on under-registered wards",
                    "suggested_schemes": self._match_schemes(schemes_db, ["ward", "development"]),
                    "estimated_cost": "Ward-level budget",
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
            "affected_count": total_population,
            "evidence": {
                "total_households": total_households,
                "total_population": total_population,
                "registration_rate": round((total_population / expected_population) * 100, 2) if expected_population > 0 else 0
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
