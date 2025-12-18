"""Course models"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class CourseType(str, enum.Enum):
    """Types of courses offered"""
    FUNDAMENTALS = "fundamentals"
    CCP_KSA = "ccp_ksa"  # Clinical Coding Professional - KSA
    CCC_PREP = "ccc_prep"
    SPECIALIZATION = "specialization"
    BOOTCAMP = "bootcamp"


class Course(Base):
    """Course model with Saudi-specific fields"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    title_ar = Column(String(500), nullable=False)
    description = Column(Text)
    description_ar = Column(Text)
    
    # Course classification
    course_type = Column(Enum(CourseType), nullable=False)
    code = Column(String(50), unique=True, index=True)
    
    # Saudi regulatory compliance
    is_chi_accredited = Column(Boolean, default=False)
    chi_accreditation_number = Column(String(100))
    meets_moh_requirements = Column(Boolean, default=False)
    scfhs_approved = Column(Boolean, default=False)
    
    # Coding systems covered
    covers_icd10am = Column(Boolean, default=False)
    covers_sbs = Column(Boolean, default=False)
    covers_ardrg = Column(Boolean, default=False)
    
    # Training modalities supported
    supports_virtual_live = Column(Boolean, default=False)
    supports_self_paced = Column(Boolean, default=False)
    supports_bootcamp = Column(Boolean, default=False)
    
    # Duration and scheduling
    duration_weeks = Column(Integer)  # For virtual live
    sessions_per_week = Column(Integer)
    hours_per_session = Column(Float)
    max_duration_months = Column(Integer)  # For self-paced
    
    # Pricing (SAR)
    price_basic = Column(Float)
    price_standard = Column(Float)
    price_premium = Column(Float)
    price_corporate = Column(Float)
    
    # Content
    syllabus = Column(JSON)
    learning_objectives = Column(JSON)
    prerequisites = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    modules = relationship("CourseModule", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    assessments = relationship("Assessment", back_populates="course")


class CourseModule(Base):
    """Course modules and competencies"""
    __tablename__ = "course_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    title = Column(String(500), nullable=False)
    title_ar = Column(String(500), nullable=False)
    description = Column(Text)
    description_ar = Column(Text)
    
    # Module ordering
    order = Column(Integer, nullable=False)
    
    # Competencies
    competencies = Column(JSON)  # List of competencies covered
    
    # Content
    content_url = Column(String(500))
    video_url = Column(String(500))
    duration_minutes = Column(Integer)
    
    # Requirements
    is_mandatory = Column(Boolean, default=True)
    passing_score = Column(Integer, default=70)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="modules")
