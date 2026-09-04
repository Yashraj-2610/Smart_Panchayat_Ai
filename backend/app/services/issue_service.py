import uuid
from sqlalchemy.orm import Session
from ..models.issue import Issue, IssueStatus, IssuePriority
from ..models.household import Household
from ..api.schemas import IssueCreate
from fastapi import HTTPException

class IssueService:
    @staticmethod
    def generate_issue_id(category: str) -> str:
        prefix = category[:3].upper() if category else "ISS"
        return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def create_issue(db: Session, household_id: int, issue_in: IssueCreate) -> Issue:
        household = db.query(Household).filter(Household.id == household_id).first()
        if not household:
            raise HTTPException(status_code=404, detail="Household not found")

        # Determine default priority based on category
        priority = IssuePriority.MEDIUM
        if issue_in.category in ["Water", "Health"]:
            priority = IssuePriority.HIGH
        elif issue_in.affected_count and issue_in.affected_count > 10:
            priority = IssuePriority.HIGH

        issue = Issue(
            issue_id=IssueService.generate_issue_id(issue_in.category.value),
            household_id=household_id,
            category=issue_in.category,
            title=issue_in.title,
            description=issue_in.description,
            status=IssueStatus.SUBMITTED,
            priority=priority,
            affected_count=issue_in.affected_count,
            language=issue_in.language
        )

        db.add(issue)
        db.commit()
        db.refresh(issue)
        return issue

    @staticmethod
    def get_all_issues(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Issue).offset(skip).limit(limit).all()

    @staticmethod
    def get_issues_by_ward(db: Session, ward_id: int):
        return db.query(Issue).join(Household).filter(Household.ward_id == ward_id).all()

    @staticmethod
    def get_issues_by_category(db: Session, category: str):
        return db.query(Issue).filter(Issue.category == category).all()

    @staticmethod
    def update_issue_status(db: Session, issue_id: int, new_status: IssueStatus):
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        issue.status = new_status
        db.commit()
        db.refresh(issue)
        return issue
