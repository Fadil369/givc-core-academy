"""Course management endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models.course import Course
from ...models.user import User
from ...core.dependencies import get_current_user

router = APIRouter()


@router.get("/")
def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all active courses"""
    courses = db.query(Course).filter(
        Course.is_active == True,
        Course.is_published == True
    ).offset(skip).limit(limit).all()
    return courses


@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get course by ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
