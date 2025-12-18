"""Adaptive Learning Engine"""
from typing import Dict, List
from ..models.user import User
from ..models.enrollment import SubscriptionTier


class AdaptiveLearningEngine:
    """AI-powered adaptive learning recommendations"""
    
    @staticmethod
    def recommend_tier(user: User, course_id: int) -> SubscriptionTier:
        """Recommend subscription tier based on user profile"""
        # Basic recommendation logic
        # In production, this would use ML models
        
        if user.user_type.value == "corporate":
            return SubscriptionTier.CORPORATE
        
        if user.experience_years and user.experience_years > 5:
            return SubscriptionTier.PREMIUM
        
        if user.preferred_modality and user.preferred_modality.value == "virtual_live":
            return SubscriptionTier.PREMIUM
        
        return SubscriptionTier.STANDARD
    
    @staticmethod
    def create_personalized_path(user: User, course_modules: List) -> List[Dict]:
        """Create personalized learning path"""
        # Simple path creation
        # In production, this would analyze user's background and learning style
        
        path = []
        for idx, module in enumerate(course_modules):
            path.append({
                "module_id": module.id,
                "order": idx + 1,
                "estimated_duration": module.duration_minutes,
                "is_mandatory": module.is_mandatory
            })
        
        return path
    
    @staticmethod
    def analyze_progress(enrollment) -> Dict:
        """Analyze user progress and provide recommendations"""
        progress = {
            "overall_progress": enrollment.progress_percentage,
            "icd10am_mastery": enrollment.icd10am_mastery,
            "sbs_mastery": enrollment.sbs_mastery,
            "ardrg_mastery": enrollment.ardrg_mastery,
            "recommendations": []
        }
        
        # Add recommendations based on progress
        if enrollment.icd10am_mastery < 70:
            progress["recommendations"].append({
                "area": "ICD-10-AM",
                "message": "Focus more on ICD-10-AM coding practice",
                "priority": "high"
            })
        
        if enrollment.sbs_mastery < 70:
            progress["recommendations"].append({
                "area": "SBS",
                "message": "Additional practice needed for Saudi Billing System",
                "priority": "high"
            })
        
        return progress
