"""Payment Service for Stripe integration"""
from typing import Dict, Optional
from ..config import settings


class PaymentService:
    """Service for handling payments with Stripe"""
    
    @staticmethod
    def create_payment_intent(
        amount: float,
        currency: str = "SAR",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Create a Stripe payment intent"""
        # In production, integrate with Stripe SDK
        # For now, return simulated response
        
        return {
            "payment_intent_id": f"pi_simulated_{amount}",
            "client_secret": "simulated_secret",
            "amount": amount,
            "currency": currency,
            "status": "requires_payment_method"
        }
    
    @staticmethod
    def calculate_total_with_vat(amount: float) -> Dict:
        """Calculate total amount including VAT"""
        vat_amount = amount * settings.VAT_RATE
        total_amount = amount + vat_amount
        
        return {
            "subtotal": amount,
            "vat_rate": settings.VAT_RATE,
            "vat_amount": round(vat_amount, 2),
            "total": round(total_amount, 2),
            "currency": "SAR"
        }
    
    @staticmethod
    def apply_corporate_discount(
        amount: float,
        seat_count: int
    ) -> float:
        """Apply corporate discount based on seat count"""
        if seat_count >= 50:
            return amount * 0.70  # 30% discount
        elif seat_count >= 20:
            return amount * 0.80  # 20% discount
        elif seat_count >= 10:
            return amount * 0.90  # 10% discount
        return amount
