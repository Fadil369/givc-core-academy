"""
Security utilities for HIPAA compliance
"""

from cryptography.fernet import Fernet
from passlib.context import CryptContext
from shared.config.settings import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_phi(data: str) -> str:
    """Encrypt PHI data"""
    f = Fernet(settings.security.encryption_key.encode())
    return f.encrypt(data.encode()).decode()


def decrypt_phi(encrypted_data: str) -> str:
    """Decrypt PHI data"""
    f = Fernet(settings.security.encryption_key.encode())
    return f.decrypt(encrypted_data.encode()).decode()


def hash_password(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)
