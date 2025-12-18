"""Payment endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ...database import get_db
from ...models.payment import Payment, PaymentStatus
from ...models.user import User
from ...core.dependencies import get_current_user
from ...config import settings

router = APIRouter()


@router.post("/create-payment-intent")
def create_payment_intent(
    amount: float,
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a payment intent"""
    # Calculate VAT
    vat_amount = amount * settings.VAT_RATE
    total_amount = amount + vat_amount
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=amount,
        vat_amount=vat_amount,
        total_amount=total_amount,
        currency="SAR",
        status=PaymentStatus.PENDING,
        enrollment_id=enrollment_id
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    # In production, integrate with Stripe here
    # For now, return simulated payment intent
    return {
        "payment_id": payment.id,
        "amount": amount,
        "vat_amount": vat_amount,
        "total_amount": total_amount,
        "currency": "SAR",
        "status": "pending"
    }


@router.get("/my-payments")
def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's payments"""
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).all()
    return payments
