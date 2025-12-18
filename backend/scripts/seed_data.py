"""Seed database with sample data"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import User, Course, CourseType, UserType
from app.core.security import get_password_hash

def seed_database():
    """Seed the database with sample data"""
    init_db()
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            email="admin@givc.sa",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            full_name_ar="مستخدم الإدارة",
            user_type=UserType.ADMIN,
            is_active=True,
            is_verified=True,
            preferred_language="ar"
        )
        db.add(admin)
        
        # Create sample student
        student = User(
            email="student@example.com",
            hashed_password=get_password_hash("student123"),
            full_name="Test Student",
            full_name_ar="طالب تجريبي",
            user_type=UserType.STUDENT,
            is_active=True,
            is_verified=True,
            preferred_language="ar",
            saudi_national_id="1234567890"
        )
        db.add(student)
        
        # Create sample course
        course = Course(
            title="Clinical Coding Professional - KSA",
            title_ar="محترف الترميز السريري - المملكة العربية السعودية",
            description="Comprehensive training for ICD-10-AM, SBS, and AR-DRG coding systems",
            description_ar="تدريب شامل لأنظمة الترميز ICD-10-AM و SBS و AR-DRG",
            course_type=CourseType.CCP_KSA,
            code="CCP-KSA-001",
            is_chi_accredited=True,
            meets_moh_requirements=True,
            covers_icd10am=True,
            covers_sbs=True,
            covers_ardrg=True,
            supports_virtual_live=True,
            supports_self_paced=True,
            duration_weeks=14,
            sessions_per_week=2,
            hours_per_session=3,
            price_basic=2500.0,
            price_standard=6000.0,
            price_premium=10000.0,
            price_corporate=8000.0,
            is_active=True,
            is_published=True
        )
        db.add(course)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print("\nSample credentials:")
        print("  Admin: admin@givc.sa / admin123")
        print("  Student: student@example.com / student123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
