"""User model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class UserType(str, enum.Enum):
    """User types in the system"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    CORPORATE = "corporate"


class TrainingModality(str, enum.Enum):
    """Preferred training modality"""
    VIRTUAL_LIVE = "virtual_live"
    SELF_PACED = "self_paced"
    BOOTCAMP = "bootcamp"
    BLENDED = "blended"


class User(Base):
    """User model with Saudi-specific fields"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    full_name_ar = Column(String(255))  # Arabic name
    
    # User classification
    user_type = Column(Enum(UserType), default=UserType.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Saudi-specific fields
    saudi_national_id = Column(String(10), unique=True, index=True)  # National ID or Iqama
    phone_number = Column(String(20))
    
    # MFA
    mfa_secret = Column(String(255))
    mfa_enabled = Column(Boolean, default=False)
    
    # Training preferences
    preferred_modality = Column(Enum(TrainingModality))
    preferred_language = Column(String(10), default="ar")  # ar or en
    
    # Professional info
    organization = Column(String(255))
    job_title = Column(String(255))
    experience_years = Column(Integer)
    
    # Metadata
    profile_data = Column(JSON)  # Additional flexible data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    assessments = relationship("UserAssessment", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    
    # Audit fields
    created_by = Column(Integer)
    updated_by = Column(Integer)
