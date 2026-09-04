from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models.household import Household
from ..models.family_member import FamilyMember
from ..models.ward import Ward

class PopulationAgent(BaseAgent):
    """Analyzes population and demographic data"""

    def __init__(self):
        super().__init__("Population & Demography Agent", "Population")

    def analyze(self, db: Session, context: Dict[str, Any]) -> Dict[str, Any]:
        total_households = db.query(func.count(Household.id)).scalar() or 0
        total_population = db.query(func.count(FamilyMember.id)).scalar() or 0

        issues_found = []
        severity = "low"

        # Check for low registration coverage (example threshold)
        expected_population = context.get("expected_population", 8000)
        if total_population < expected_population * 0.5:
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

        if ward_populations and max(ward_populations) > 2 * min(ward_populations):
            issues_found.append({
                "issue": "Significant population imbalance across wards",
                "description": "Some wards are much more populated than others",
                "impact": "Unequal resource distribution"
            })

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
            "recommendations": [
                "Increase household registration drives",
                "Focus on under-registered wards"
            ] if issues_found else []
        }
