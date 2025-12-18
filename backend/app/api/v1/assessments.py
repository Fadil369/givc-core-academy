"""Assessment endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ...database import get_db
from ...models.assessment import Assessment, UserAssessment
from ...models.user import User
from ...core.dependencies import get_current_user

router = APIRouter()


@router.get("/course/{course_id}")
def list_course_assessments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List assessments for a course"""
    assessments = db.query(Assessment).filter(
        Assessment.course_id == course_id,
        Assessment.is_active == True
    ).all()
    return assessments


@router.post("/{assessment_id}/start")
def start_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start an assessment attempt"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Check attempt count
    attempts = db.query(UserAssessment).filter(
        UserAssessment.user_id == current_user.id,
        UserAssessment.assessment_id == assessment_id
    ).count()
    
    if attempts >= assessment.max_attempts:
        raise HTTPException(status_code=400, detail="Maximum attempts reached")
    
    # Create user assessment
    user_assessment = UserAssessment(
        user_id=current_user.id,
        assessment_id=assessment_id,
        attempt_number=attempts + 1,
        started_at=datetime.utcnow()
    )
    
    db.add(user_assessment)
    db.commit()
    db.refresh(user_assessment)
    
    return user_assessment


@router.get("/my-results")
def get_my_assessment_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's assessment results"""
    results = db.query(UserAssessment).filter(
        UserAssessment.user_id == current_user.id
    ).all()
    return results
