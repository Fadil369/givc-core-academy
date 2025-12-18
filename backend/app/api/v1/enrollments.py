"""Enrollment endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ...database import get_db
from ...models.enrollment import Enrollment, EnrollmentStatus, SubscriptionTier
from ...models.user import User
from ...models.course import Course
from ...core.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def create_enrollment(
    course_id: int,
    subscription_tier: SubscriptionTier,
    modality: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in a course"""
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id,
        Enrollment.status.in_([EnrollmentStatus.PENDING, EnrollmentStatus.ACTIVE])
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # Create enrollment
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        subscription_tier=subscription_tier,
        modality=modality,
        status=EnrollmentStatus.PENDING,
        enrolled_at=datetime.utcnow()
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment


@router.get("/my-enrollments")
def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's enrollments"""
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()
    return enrollments
