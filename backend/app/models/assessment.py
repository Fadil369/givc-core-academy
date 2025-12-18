"""Assessment models"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, JSON, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class AssessmentType(str, enum.Enum):
    """Types of assessments"""
    QUIZ = "quiz"
    EXAM = "exam"
    ICD10AM_SIMULATION = "icd10am_simulation"
    SBS_PRACTICE = "sbs_practice"
    ARDRG_EXERCISE = "ardrg_exercise"
    CASE_STUDY = "case_study"


class Assessment(Base):
    """Assessment/exam configuration"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    title = Column(String(500), nullable=False)
    title_ar = Column(String(500), nullable=False)
    description = Column(Text)
    description_ar = Column(Text)
    
    # Assessment type
    assessment_type = Column(Enum(AssessmentType), nullable=False)
    
    # Configuration
    time_limit_minutes = Column(Integer)
    passing_score = Column(Integer, default=70)
    max_attempts = Column(Integer, default=3)
    
    # Saudi coding systems focus
    focuses_on_icd10am = Column(Boolean, default=False)
    focuses_on_sbs = Column(Boolean, default=False)
    focuses_on_ardrg = Column(Boolean, default=False)
    
    # Questions
    total_questions = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="assessments")
    questions = relationship("Question", back_populates="assessment")
    user_assessments = relationship("UserAssessment", back_populates="assessment")


class Question(Base):
    """Assessment questions"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    
    question_text = Column(Text, nullable=False)
    question_text_ar = Column(Text, nullable=False)
    
    # Question type (mcq, coding, case-based)
    question_type = Column(String(50), nullable=False)
    
    # For MCQ
    options = Column(JSON)  # List of options with correct answer marked
    
    # For coding questions
    medical_case = Column(JSON)  # Anonymized medical case data
    correct_codes = Column(JSON)  # Correct ICD/SBS/DRG codes
    
    # Difficulty and points
    difficulty = Column(String(20))  # easy, medium, hard
    points = Column(Integer, default=1)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    assessment = relationship("Assessment", back_populates="questions")


class UserAssessment(Base):
    """User assessment attempts and results"""
    __tablename__ = "user_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    
    # Attempt tracking
    attempt_number = Column(Integer, default=1)
    
    # Results
    score = Column(Float)
    total_possible_score = Column(Float)
    percentage = Column(Float)
    passed = Column(Boolean)
    
    # Answers
    answers = Column(JSON)  # User's answers
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    time_taken_minutes = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    assessment = relationship("Assessment", back_populates="user_assessments")
