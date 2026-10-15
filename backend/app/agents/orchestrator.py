from typing import Dict, Any, List
from sqlalchemy.orm import Session
from .water_agent import WaterAgent
from .health_agent import HealthAgent
from .education_agent import EducationAgent
from .population_agent import PopulationAgent
from .infrastructure_agent import InfrastructureAgent
from .priority_agent import PriorityAgent
from .predictive_agent import PredictiveAnalyticsAgent

class MultiAgentOrchestrator:
    """
    Central orchestration layer for multi-agent system
    Coordinates all specialized agents and combines their analysis

    Enhanced with:
    - Confidence-weighted analysis
    - Predictive analytics agent
    - Trend forecasting
    - Enhanced explainability
    """

    def __init__(self):
        self.agents = [
            PopulationAgent(),
            WaterAgent(),
            HealthAgent(),
            EducationAgent(),
            InfrastructureAgent(),
            PredictiveAnalyticsAgent(),
        ]
        self.priority_agent = PriorityAgent()

    def run_analysis(self, db: Session, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run all agents and produce consolidated recommendations
        Enhanced with confidence scores and predictive insights
        """
        if context is None:
            context = {}

        # Fetch schemes for RAG matching
        if "schemes_db" not in context:
            context["schemes_db"] = self._fetch_schemes_for_rag(db)

        agent_results = []

        # Run each specialized agent
        for agent in self.agents:
            try:
                result = agent.analyze(db, context)
                # Track confidence score
                result["_confidence_weight"] = result.get("confidence_score", 0.5)
                agent_results.append(result)
            except Exception as e:
                # Log error but continue with other agents
                agent_results.append({
                    "agent_name": agent.name,
                    "domain": agent.domain,
                    "error": str(e),
                    "severity": "unknown",
                    "affected_count": 0,
                    "issues_found": [],
                    "confidence_score": 0.0,
                })

        # Run priority scoring
        priority_context = {"agent_results": agent_results}
        priority_result = self.priority_agent.analyze(db, priority_context)

        # Combine recommendations from all agents
        all_recommendations = []
        all_recommendations_with_schemes = []

        for result in agent_results:
            all_recommendations.extend(result.get("recommendations", []))
            # Collect enhanced recommendations with schemes
            if result.get("recommendations_with_schemes"):
                all_recommendations_with_schemes.extend(result["recommendations_with_schemes"])

        # Add priority-based recommendations
        scored_issues = priority_result.get("scored_issues", [])
        priority_recommendations = self.priority_agent.get_priority_recommendations(scored_issues)

        # Enhanced summary with confidence-weighted insights
        summary = self._generate_summary(agent_results, priority_result)

        return {
            "analysis_type": "Multi-Agent Village Analysis",
            "agent_results": agent_results,
            "priority_analysis": priority_result,
            "top_priority_domain": priority_result.get("top_priority_domain"),
            "all_recommendations": all_recommendations,
            "priority_recommendations": priority_recommendations,
            "recommendations_with_schemes": all_recommendations_with_schemes,
            "summary": summary,
            "analysis_metadata": {
                "total_agents": len(agent_results),
                "successful_agents": len([r for r in agent_results if "error" not in r]),
                "confidence_avg": self._calculate_avg_confidence(agent_results),
                "domains_analyzed": [r.get("domain") for r in agent_results],
            }
        }

    def _fetch_schemes_for_rag(self, db: Session) -> List[Dict]:
        """Fetch all schemes for recommendation matching"""
        try:
            from ..services.rag_service import RAGService
            schemes = RAGService.GOVERNMENT_SCHEMES_DATA or []
            # Convert to dict format for matching
            return [
                {
                    "scheme_id": s.get("scheme_id", ""),
                    "name": s.get("name", ""),
                    "category": s.get("category", ""),
                    "level": s.get("level", ""),
                    "description": s.get("description", ""),
                    "eligibility_criteria": s.get("eligibility_criteria", ""),
                    "benefits": s.get("benefits", ""),
                    "official_link": s.get("official_link", ""),
                }
                for s in schemes
            ]
        except Exception:
            return []

    def _calculate_avg_confidence(self, agent_results: List[Dict]) -> float:
        """Calculate average confidence across all agent results"""
        confidences = [r.get("_confidence_weight", 0.5) for r in agent_results if "error" not in r]
        return round(sum(confidences) / len(confidences), 3) if confidences else 0.0

    def _generate_summary(self, agent_results: List[Dict], priority_result: Dict) -> str:
        """Generate human-readable summary with confidence information"""
        # Count issues across all agents
        total_issues = sum(len(r.get("issues_found", [])) for r in agent_results)
        # Filter out error agents for severity calc
        valid_results = [r for r in agent_results if "error" not in r]
        high_severity_count = sum(
            1 for r in valid_results
            if r.get("severity") in ["high", "critical"]
        )

        top_domain = priority_result.get("top_priority_domain", "Unknown")
        avg_confidence = self._calculate_avg_confidence(agent_results)

        summary = (
            f"Village Analysis Summary:\n"
            f"- Total issues identified across all domains: {total_issues}\n"
            f"- High/Critical severity domains: {high_severity_count}\n"
            f"- Top priority domain: {top_domain}\n"
            f"- Average confidence score: {avg_confidence}/1.0\n"
        )

        if high_severity_count > 0:
            summary += f"\n🚨 Immediate attention required in {high_severity_count} domain(s)."

        # Add predictive insights if available
        predictive_results = [r for r in valid_results if r.get("domain") == "Predictive"]
        if predictive_results:
            preds = predictive_results[0].get("predictions", [])
            if preds:
                summary += f"\n\n🔮 Predictive Insights:\n"
                for pred in preds[:3]:
                    summary += (
                        f"- {pred.get('prediction', 'N/A')} "
                        f"(Probability: {pred.get('probability', 0):.0%})\n"
                    )

        return summary

    def get_trend_analysis(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """
        Get trend analysis for dashboard visualizations
        Returns time-series data for charts
        """
        from ..models.issue import Issue
        from ..models.household import Household
        from datetime import datetime, timedelta
        from sqlalchemy import func

        # Daily issue trend for past N days
        daily_trends = []
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            count = db.query(func.count(Issue.id)).filter(
                Issue.created_at >= date,
                Issue.created_at < date + timedelta(days=1)
            ).scalar() or 0
            daily_trends.append({
                "date": date.strftime("%Y-%m-%d"),
                "count": count
            })

        return {
            "period_days": days,
            "daily_issue_trend": daily_trends,
            "total_issues": sum(d["count"] for d in daily_trends),
        }

    def get_domain_comparison(self, agent_results: List[Dict]) -> List[Dict]:
        """
        Generate domain comparison data for visualization
        Compares severity scores across domains
        """
        severity_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}

        comparison = []
        for result in agent_results:
            if "error" in result:
                continue
            comparison.append({
                "domain": result.get("domain"),
                "severity": result.get("severity", "low"),
                "severity_score": severity_scores.get(result.get("severity", "low"), 0),
                "affected_count": result.get("affected_count", 0),
                "issues_count": len(result.get("issues_found", [])),
                "confidence": result.get("confidence_score", 0.0),
            })

        comparison.sort(key=lambda x: x["severity_score"], reverse=True)
        return comparison