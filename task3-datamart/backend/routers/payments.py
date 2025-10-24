from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Dataset, Purchase
from auth_utils import get_current_user
from stripe_service import StripeService

router = APIRouter()

class PaymentRequest(BaseModel):
    dataset_id: int
    rows_requested: int
    filters: dict = {}

class PaymentResponse(BaseModel):
    payment_intent_id: str
    client_secret: str
    amount_cents: int
    purchase_id: int

@router.post("/create-payment-intent", response_model=PaymentResponse)
async def create_payment_intent(
    payment_request: PaymentRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe payment intent for dataset purchase"""
    
    # Validate dataset
    dataset = db.query(Dataset).filter(Dataset.id == payment_request.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Calculate cost
    total_cost = payment_request.rows_requested * dataset.price_per_row
    amount_cents = int(total_cost * 100)  # Convert to cents
    
    # Create pending purchase record
    purchase = Purchase(
        user_id=current_user.id,
        dataset_id=payment_request.dataset_id,
        rows_purchased=payment_request.rows_requested,
        total_cost=total_cost,
        filters_applied=payment_request.filters,
        status="pending"
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    
    # Create Stripe payment intent
    payment_intent = StripeService.create_payment_intent(
        amount_cents=amount_cents,
        metadata={
            "purchase_id": str(purchase.id),
            "user_id": str(current_user.id),
            "dataset_id": str(payment_request.dataset_id),
            "rows": str(payment_request.rows_requested)
        }
    )
    
    return PaymentResponse(
        payment_intent_id=payment_intent.id,
        client_secret=payment_intent.client_secret,
        amount_cents=amount_cents,
        purchase_id=purchase.id
    )

@router.post("/confirm-payment/{purchase_id}")
async def confirm_payment(
    purchase_id: int,
    payment_intent_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Confirm payment and update purchase status"""
    
    # Verify purchase belongs to user
    purchase = db.query(Purchase).filter(
        Purchase.id == purchase_id,
        Purchase.user_id == current_user.id,
        Purchase.status == "pending"
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Verify payment with Stripe
    if StripeService.confirm_payment(payment_intent_id):
        purchase.status = "completed"
        purchase.payment_intent_id = payment_intent_id
        db.commit()
        
        return {
            "success": True,
            "purchase_id": purchase.id,
            "download_url": f"/datasets/{purchase.dataset_id}/download/{purchase.id}",
            "message": "Payment successful! You can now download your data."
        }
    else:
        purchase.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail="Payment failed")

@router.get("/webhook")
async def stripe_webhook():
    """Handle Stripe webhooks for payment confirmation"""
    # In a real app, this would handle Stripe webhook events
    # to automatically update purchase status
    return {"message": "Webhook endpoint - implement based on your needs"}