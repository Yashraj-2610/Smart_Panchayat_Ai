from typing import Dict, Any, List
from sqlalchemy.orm import Session
from .water_agent import WaterAgent
from .health_agent import HealthAgent
from .education_agent import EducationAgent
from .population_agent import PopulationAgent
from .infrastructure_agent import InfrastructureAgent
from .priority_agent import PriorityAgent

class MultiAgentOrchestrator:
    """
    Central orchestration layer for multi-agent system
    Coordinates all specialized agents and combines their analysis
    """

    def __init__(self):
        self.agents = [
            PopulationAgent(),
            WaterAgent(),
            HealthAgent(),
            EducationAgent(),
            InfrastructureAgent()
        ]
        self.priority_agent = PriorityAgent()

    def run_analysis(self, db: Session, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run all agents and produce consolidated recommendations
        """
        if context is None:
            context = {}

        agent_results = []

        # Run each specialized agent
        for agent in self.agents:
            try:
                result = agent.analyze(db, context)
                agent_results.append(result)
            except Exception as e:
                # Log error but continue with other agents
                agent_results.append({
                    "agent_name": agent.name,
                    "domain": agent.domain,
                    "error": str(e),
                    "severity": "unknown",
                    "affected_count": 0,
                    "issues_found": []
                })

        # Run priority scoring
        priority_context = {"agent_results": agent_results}
        priority_result = self.priority_agent.analyze(db, priority_context)

        # Combine recommendations from all agents
        all_recommendations = []
        for result in agent_results:
            all_recommendations.extend(result.get("recommendations", []))

        # Add priority-based recommendations
        scored_issues = priority_result.get("scored_issues", [])
        priority_recommendations = self.priority_agent.get_priority_recommendations(scored_issues)

        return {
            "analysis_type": "Multi-Agent Village Analysis",
            "agent_results": agent_results,
            "priority_analysis": priority_result,
            "top_priority_domain": priority_result.get("top_priority_domain"),
            "all_recommendations": all_recommendations,
            "priority_recommendations": priority_recommendations,
            "summary": self._generate_summary(agent_results, priority_result)
        }

    def _generate_summary(self, agent_results: List[Dict], priority_result: Dict) -> str:
        """Generate human-readable summary"""
        total_issues = sum(len(r.get("issues_found", [])) for r in agent_results)
        top_domain = priority_result.get("top_priority_domain", "Unknown")

        high_severity_count = sum(1 for r in agent_results if r.get("severity") in ["high", "critical"])

        summary = f"Village Analysis Summary:\n"
        summary += f"- Total issues identified across all domains: {total_issues}\n"
        summary += f"- High/Critical severity domains: {high_severity_count}\n"
        summary += f"- Top priority domain: {top_domain}\n"

        if high_severity_count > 0:
            summary += f"\nImmediate attention required in {high_severity_count} domain(s)."

        return summary
