from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Purchase
from schemas import UserProfile, PurchaseHistory
from auth_utils import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at
    )

@router.get("/purchases", response_model=List[PurchaseHistory])
async def get_user_purchases(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's purchase history"""
    purchases = db.query(Purchase).filter(
        Purchase.user_id == current_user.id
    ).order_by(Purchase.created_at.desc()).all()
    
    purchase_history = []
    for purchase in purchases:
        purchase_history.append(PurchaseHistory(
            id=purchase.id,
            dataset_id=purchase.dataset_id,
            dataset_name=purchase.dataset.name,
            rows_purchased=purchase.rows_purchased,
            total_cost=purchase.total_cost,
            status=purchase.status,
            created_at=purchase.created_at,
            download_url=f"/datasets/{purchase.dataset_id}/download/{purchase.id}" if purchase.status == "completed" else None
        ))
    
    return purchase_history

@router.get("/stats")
async def get_user_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    total_purchases = db.query(Purchase).filter(
        Purchase.user_id == current_user.id
    ).count()
    
    total_spent = db.query(Purchase).filter(
        Purchase.user_id == current_user.id,
        Purchase.status == "completed"
    ).with_entities(Purchase.total_cost).all()
    
    total_amount = sum([purchase.total_cost for purchase in total_spent])
    
    total_rows = db.query(Purchase).filter(
        Purchase.user_id == current_user.id,
        Purchase.status == "completed"
    ).with_entities(Purchase.rows_purchased).all()
    
    total_rows_purchased = sum([purchase.rows_purchased for purchase in total_rows])
    
    return {
        "total_purchases": total_purchases,
        "total_spent": float(total_amount),
        "total_rows_purchased": total_rows_purchased
    }