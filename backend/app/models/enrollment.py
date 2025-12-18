"""Enrollment models"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class SubscriptionTier(str, enum.Enum):
    """Subscription tiers"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    CORPORATE = "corporate"


class EnrollmentStatus(str, enum.Enum):
    """Enrollment status"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class Enrollment(Base):
    """User course enrollment"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Subscription details
    subscription_tier = Column(Enum(SubscriptionTier), nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.PENDING)
    
    # Training modality for this enrollment
    modality = Column(String(50))
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    completed_modules = Column(JSON, default=list)
    
    # Saudi-specific metrics
    icd10am_mastery = Column(Float, default=0.0)
    sbs_mastery = Column(Float, default=0.0)
    ardrg_mastery = Column(Float, default=0.0)
    
    # Adaptive learning data
    learning_path = Column(JSON)  # Personalized learning path
    recommended_tier = Column(String(50))
    
    # Dates
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Corporate enrollment info
    corporate_account_id = Column(Integer)
    is_bulk_enrollment = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
