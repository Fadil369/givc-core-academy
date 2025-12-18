"""Analytics Service for dashboard metrics"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from ..models.user import User, UserType
from ..models.enrollment import Enrollment, EnrollmentStatus
from ..models.payment import Payment, PaymentStatus
from ..models.course import Course


class AnalyticsService:
    """Service for generating analytics and metrics"""
    
    @staticmethod
    def get_individual_learner_metrics(db: Session) -> Dict:
        """Get metrics for individual learners"""
        total_students = db.query(User).filter(
            User.user_type == UserType.STUDENT
        ).count()
        
        active_enrollments = db.query(Enrollment).filter(
            Enrollment.status == EnrollmentStatus.ACTIVE
        ).count()
        
        completed_enrollments = db.query(Enrollment).filter(
            Enrollment.status == EnrollmentStatus.COMPLETED
        ).count()
        
        completion_rate = (
            (completed_enrollments / active_enrollments * 100)
            if active_enrollments > 0 else 0
        )
        
        return {
            "total_students": total_students,
            "active_enrollments": active_enrollments,
            "completed_enrollments": completed_enrollments,
            "completion_rate": round(completion_rate, 2)
        }
    
    @staticmethod
    def get_corporate_metrics(db: Session) -> Dict:
        """Get metrics for corporate accounts"""
        corporate_users = db.query(User).filter(
            User.user_type == UserType.CORPORATE
        ).count()
        
        corporate_enrollments = db.query(Enrollment).filter(
            Enrollment.is_bulk_enrollment == True
        ).count()
        
        return {
            "corporate_accounts": corporate_users,
            "corporate_enrollments": corporate_enrollments
        }
    
    @staticmethod
    def get_platform_metrics(db: Session) -> Dict:
        """Get overall platform metrics"""
        total_users = db.query(User).count()
        total_courses = db.query(Course).filter(Course.is_active == True).count()
        total_enrollments = db.query(Enrollment).count()
        
        # Revenue calculation
        total_revenue = db.query(
            func.sum(Payment.total_amount)
        ).filter(
            Payment.status == PaymentStatus.COMPLETED
        ).scalar() or 0
        
        return {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_enrollments": total_enrollments,
            "total_revenue_sar": round(total_revenue, 2)
        }
