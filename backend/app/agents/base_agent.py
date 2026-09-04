from abc import ABC, abstractmethod
from typing import Dict, Any, List
from sqlalchemy.orm import Session

class BaseAgent(ABC):
    """
    Base class for all specialized domain agents
    Each agent analyzes a specific development domain
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
            "recommendations": List[str]
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

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.utcnow()
