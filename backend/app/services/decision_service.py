import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models.issue import Issue, IssuePriority
from ..models.household import Household
from ..models.recommendation import AIRecommendation, RecommendationStatus
from ..agents.orchestrator import MultiAgentOrchestrator
from .rag_service import RAGService
from .multilingual_service import MultilingualService

class DecisionSupportService:
    """
    Decision Support and Explainability Engine
    Takes multi-agent findings, prioritizes problems, queries RAG for schemes,
    and produces explainable recommendations for Sarpanch / Panchayat officials.
    """

    @staticmethod
    def generate_recommendations_for_all_issues(db: Session) -> List[AIRecommendation]:
        orchestrator = MultiAgentOrchestrator()
        analysis = orchestrator.run_analysis(db)

        # Get all unresolved issues
        issues = db.query(Issue).filter(Issue.status.in_(["Submitted", "Under Review"])).all()
        created_recs = []

        for issue in issues:
            # Check if recommendation already exists
            existing = db.query(AIRecommendation).filter(AIRecommendation.issue_id == issue.id).first()
            if existing:
                continue

            # Query RAG for schemes
            relevant_schemes = RAGService.retrieve_relevant_schemes(
                query=f"{issue.title} {issue.description}",
                domain=issue.category.value,
                top_k=2
            )

            # Calculate priority score
            category_weights = {
                "Health": 85.0,
                "Water": 90.0,
                "Sanitation": 80.0,
                "Road & Infrastructure": 65.0,
                "Education": 75.0,
                "Agriculture": 70.0,
                "Electricity": 60.0,
                "Other": 40.0
            }
            base = category_weights.get(issue.category.value, 50.0)
            affected_bonus = min(issue.affected_count * 2.0, 30.0)
            priority_score = min(base + affected_bonus, 100.0)

            # Generate Explainable Recommendation Text
            schemes_text = ", ".join([s["name"] for s in relevant_schemes]) if relevant_schemes else "Gram Panchayat Local Development Fund"
            rec_text = (
                f"Action Recommended for '{issue.title}': "
                f"Allocate priority intervention in Ward {issue.household.ward_id}. "
                f"Apply for funding/support under {schemes_text}. "
                f"Estimated affected residents: {issue.affected_count * 4}. "
                f"Severity level assessed as {issue.priority.value}."
            )

            evidence = {
                "issue_category": issue.category.value,
                "affected_households": issue.affected_count,
                "ward_id": issue.household.ward_id,
                "calculated_priority_score": round(priority_score, 1),
                "matched_schemes": [s["name"] for s in relevant_schemes],
                "justification": f"Category {issue.category.value} has high community impact factor. {issue.affected_count} households directly impacted."
            }

            rec = AIRecommendation(
                recommendation_id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                issue_id=issue.id,
                priority_score=priority_score,
                recommendation_text=rec_text,
                evidence=evidence,
                affected_wards=[issue.household.ward_id],
                affected_households=issue.affected_count,
                suggested_schemes=[s["scheme_id"] for s in relevant_schemes],
                estimated_cost=50000.0 if issue.category.value in ["Water", "Road & Infrastructure"] else 15000.0,
                estimated_timeline="2 to 4 weeks",
                agent_analysis={"orchestrator_summary": analysis.get("summary")},
                status=RecommendationStatus.GENERATED,
                language=issue.language
            )

            db.add(rec)
            created_recs.append(rec)

        db.commit()
        return created_recs

    @staticmethod
    def get_recommendations_summary(db: Session) -> Dict[str, Any]:
        recs = db.query(AIRecommendation).all()
        return {
            "total_recommendations": len(recs),
            "high_priority_count": sum(1 for r in recs if r.priority_score >= 75),
            "recommendations": [
                {
                    "id": r.id,
                    "recommendation_id": r.recommendation_id,
                    "issue_id": r.issue_id,
                    "priority_score": r.priority_score,
                    "recommendation_text": r.recommendation_text,
                    "evidence": r.evidence,
                    "status": r.status.value,
                    "created_at": str(r.created_at)
                } for r in recs
            ]
        }
