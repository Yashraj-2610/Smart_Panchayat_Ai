from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...core.database import get_db
from ...api.schemas import (
    PopulationAnalytics, WardAnalytics, DomainAnalytics,
    IssueResponse, RecommendationResponse, WardResponse
)
from ...services.analytics_service import AnalyticsService
from ...services.issue_service import IssueService
from ...services.decision_service import DecisionSupportService
from ...agents.orchestrator import MultiAgentOrchestrator
from ...models.ward import Ward

router = APIRouter()

@router.get("/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Sarpanch Dashboard Overview
    Returns population summary, issue summary, and key indicators
    """
    population_stats = AnalyticsService.get_population_summary(db)
    issue_stats = AnalyticsService.get_issue_statistics(db)
    ward_stats = AnalyticsService.get_ward_wise_analytics(db)

    return {
        "village_name": "Alandi Gram Panchayat",
        "district": "Pune",
        "state": "Maharashtra",
        "population_summary": population_stats,
        "issue_statistics": issue_stats,
        "ward_summary": ward_stats,
        "last_updated": "2026-09-04"
    }

@router.get("/analytics/population", response_model=PopulationAnalytics)
def get_population_analytics(db: Session = Depends(get_db)):
    """Detailed population and demographic analytics"""
    return AnalyticsService.get_population_summary(db)

@router.get("/analytics/wards", response_model=List[WardAnalytics])
def get_ward_analytics(db: Session = Depends(get_db)):
    """Ward-wise breakdown of population and issues"""
    return AnalyticsService.get_ward_wise_analytics(db)

@router.get("/wards", response_model=List[WardResponse])
def list_wards(db: Session = Depends(get_db)):
    """List all wards"""
    return db.query(Ward).all()

@router.get("/issues/all", response_model=List[IssueResponse])
def get_all_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all reported issues across the village"""
    return IssueService.get_all_issues(db, skip, limit)

@router.get("/issues/ward/{ward_id}", response_model=List[IssueResponse])
def get_issues_by_ward(ward_id: int, db: Session = Depends(get_db)):
    """Get all issues in a specific ward"""
    return IssueService.get_issues_by_ward(db, ward_id)

@router.get("/issues/category/{category}")
def get_issues_by_category(category: str, db: Session = Depends(get_db)):
    """Get issues by category (Water, Health, Education, etc.)"""
    return IssueService.get_issues_by_category(db, category)

@router.post("/ai/analyze")
def run_multi_agent_analysis(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Run Multi-Agent AI Analysis on Village Data
    Executes all specialized domain agents and returns prioritized findings
    """
    orchestrator = MultiAgentOrchestrator()
    context = {"expected_population": 8000}  # Can be configured
    analysis_result = orchestrator.run_analysis(db, context)
    return analysis_result

@router.post("/ai/recommendations/generate")
def generate_ai_recommendations(db: Session = Depends(get_db)):
    """
    Generate AI recommendations for all pending issues
    Uses Multi-Agent analysis + RAG scheme matching
    """
    recommendations = DecisionSupportService.generate_recommendations_for_all_issues(db)
    return {
        "message": f"Generated {len(recommendations)} new recommendations",
        "recommendations_created": len(recommendations)
    }

@router.get("/ai/recommendations")
def get_recommendations_summary(db: Session = Depends(get_db)):
    """Get all AI recommendations with priority scores and evidence"""
    return DecisionSupportService.get_recommendations_summary(db)

@router.get("/reports/summary")
def generate_panchayat_report(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Generate comprehensive Panchayat meeting report
    Includes all analytics, top issues, and AI recommendations
    """
    population = AnalyticsService.get_population_summary(db)
    issues = AnalyticsService.get_issue_statistics(db)
    recommendations = DecisionSupportService.get_recommendations_summary(db)

    return {
        "report_title": "Gram Panchayat Development Report",
        "generated_on": "2026-09-04",
        "village": "Alandi Gram Panchayat",
        "population_statistics": population,
        "issue_statistics": issues,
        "ai_recommendations": recommendations,
        "executive_summary": (
            f"Total registered population: {population['total_population']}, "
            f"Total households: {population['total_households']}. "
            f"Active issues: {issues['total_issues']}. "
            f"High-priority AI recommendations: {recommendations['high_priority_count']}."
        )
    }
