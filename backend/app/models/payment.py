"""Payment and subscription models"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class PaymentStatus(str, enum.Enum):
    """Payment status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class Payment(Base):
    """Payment transactions"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Payment details
    amount = Column(Float, nullable=False)  # in SAR
    vat_amount = Column(Float)  # 15% VAT
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="SAR")
    
    # Payment processing
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50))
    
    # Stripe integration
    stripe_payment_intent_id = Column(String(255), unique=True)
    stripe_customer_id = Column(String(255))
    
    # Related entities
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    
    # Invoice
    invoice_number = Column(String(100), unique=True)
    invoice_url = Column(String(500))
    
    # Metadata
    payment_metadata = Column(Text)  # JSON string for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="payments")


class Subscription(Base):
    """Subscription management for CPD and recurring access"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Subscription details
    tier = Column(String(50), nullable=False)  # basic, standard, premium, corporate
    status = Column(String(50), default="active")
    
    # Pricing
    price_per_month = Column(Float)
    billing_cycle = Column(String(20))  # monthly, annual
    
    # Stripe
    stripe_subscription_id = Column(String(255), unique=True)
    stripe_customer_id = Column(String(255))
    
    # Dates
    started_at = Column(DateTime, default=datetime.utcnow)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancelled_at = Column(DateTime)
    ended_at = Column(DateTime)
    
    # Corporate subscriptions
    is_corporate = Column(Boolean, default=False)
    corporate_account_id = Column(Integer)
    max_seats = Column(Integer)
    used_seats = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
