"""User schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models.user import UserType, TrainingModality


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    full_name_ar: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)
    user_type: UserType = UserType.STUDENT
    saudi_national_id: Optional[str] = None
    phone_number: Optional[str] = None
    preferred_language: str = "ar"


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    full_name_ar: Optional[str] = None
    phone_number: Optional[str] = None
    preferred_modality: Optional[TrainingModality] = None
    preferred_language: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    experience_years: Optional[int] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    user_type: UserType
    is_active: bool
    is_verified: bool
    saudi_national_id: Optional[str]
    phone_number: Optional[str]
    preferred_modality: Optional[TrainingModality]
    preferred_language: str
    organization: Optional[str]
    job_title: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload"""
    sub: Optional[int] = None
    exp: Optional[int] = None
