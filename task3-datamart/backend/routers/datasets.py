from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io
from fastapi.responses import StreamingResponse

from database import get_db
from models import Dataset, DatasetRow, Purchase
from schemas import DatasetResponse, DatasetPreview, FilterRequest
from auth_utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[DatasetResponse])
async def get_datasets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all available datasets with pagination"""
    datasets = db.query(Dataset).offset(skip).limit(limit).all()
    return datasets

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get specific dataset details"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.post("/{dataset_id}/preview", response_model=DatasetPreview)
async def preview_dataset(
    dataset_id: int,
    filters: FilterRequest,
    db: Session = Depends(get_db)
):
    """Preview dataset with filters applied"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Build query with filters
    query = db.query(DatasetRow).filter(DatasetRow.dataset_id == dataset_id)
    
    # Apply filters based on dataset type
    if filters.filters:
        for filter_key, filter_value in filters.filters.items():
            if filter_key == "country" and filter_value:
                query = query.filter(DatasetRow.data["country"].astext == filter_value)
            elif filter_key == "min_funding" and filter_value:
                query = query.filter(DatasetRow.data["funding_amount"].astext.cast(float) >= float(filter_value))
            elif filter_key == "max_funding" and filter_value:
                query = query.filter(DatasetRow.data["funding_amount"].astext.cast(float) <= float(filter_value))
            elif filter_key == "year_from" and filter_value:
                query = query.filter(DatasetRow.data["year"].astext.cast(int) >= int(filter_value))
            elif filter_key == "year_to" and filter_value:
                query = query.filter(DatasetRow.data["year"].astext.cast(int) <= int(filter_value))
            elif filter_key == "location" and filter_value:
                query = query.filter(DatasetRow.data["location"].astext.ilike(f"%{filter_value}%"))
            elif filter_key == "min_price" and filter_value:
                query = query.filter(DatasetRow.data["price"].astext.cast(float) >= float(filter_value))
            elif filter_key == "max_price" and filter_value:
                query = query.filter(DatasetRow.data["price"].astext.cast(float) <= float(filter_value))
    
    # Get total count and preview rows
    total_rows = query.count()
    preview_rows = query.limit(10).all()
    
    return DatasetPreview(
        dataset_id=dataset_id,
        total_matching_rows=total_rows,
        preview_rows=[row.data for row in preview_rows],
        price_per_row=dataset.price_per_row
    )

@router.post("/{dataset_id}/purchase")
async def purchase_dataset(
    dataset_id: int,
    filters: FilterRequest,
    rows_requested: int = Query(..., ge=1, le=10000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Purchase dataset rows and return download link"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Calculate total cost
    total_cost = rows_requested * dataset.price_per_row
    
    # Create purchase record
    purchase = Purchase(
        user_id=current_user.id,
        dataset_id=dataset_id,
        rows_purchased=rows_requested,
        total_cost=total_cost,
        filters_applied=filters.filters or {},
        status="completed"  # In real app, this would be "pending" until payment
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    
    return {
        "purchase_id": purchase.id,
        "total_cost": total_cost,
        "rows_purchased": rows_requested,
        "download_url": f"/datasets/{dataset_id}/download/{purchase.id}",
        "message": "Purchase successful! Use the download URL to get your data."
    }

@router.get("/{dataset_id}/download/{purchase_id}")
async def download_dataset(
    dataset_id: int,
    purchase_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download purchased dataset as CSV"""
    # Verify purchase
    purchase = db.query(Purchase).filter(
        Purchase.id == purchase_id,
        Purchase.user_id == current_user.id,
        Purchase.dataset_id == dataset_id,
        Purchase.status == "completed"
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found or not authorized")
    
    # Build query with original filters
    query = db.query(DatasetRow).filter(DatasetRow.dataset_id == dataset_id)
    
    # Apply the same filters used during purchase
    if purchase.filters_applied:
        for filter_key, filter_value in purchase.filters_applied.items():
            if filter_key == "country" and filter_value:
                query = query.filter(DatasetRow.data["country"].astext == filter_value)
            elif filter_key == "min_funding" and filter_value:
                query = query.filter(DatasetRow.data["funding_amount"].astext.cast(float) >= float(filter_value))
            # Add other filters as needed...
    
    # Get the purchased number of rows
    rows = query.limit(purchase.rows_purchased).all()
    
    # Create CSV
    output = io.StringIO()
    if rows:
        # Get column names from first row
        fieldnames = list(rows[0].data.keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            writer.writerow(row.data)
    
    output.seek(0)
    
    # Return CSV as download
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=dataset_{dataset_id}_purchase_{purchase_id}.csv"}
    )