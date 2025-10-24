from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Dataset schemas
class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_row: float = 0.05

class Dataset(DatasetBase):
    id: int
    table_name: str
    total_rows: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DatasetPreview(BaseModel):
    filters: Dict[str, Any]
    limit: int = 10

class DatasetPurchase(BaseModel):
    filters: Dict[str, Any]
    rows_count: int
    stripe_token: str

# Purchase schemas
class Purchase(BaseModel):
    id: int
    dataset_id: int
    rows_purchased: int
    total_amount: float
    created_at: datetime
    download_url: Optional[str]
    dataset: Dataset
    
    class Config:
        from_attributes = True

# Data schemas
class StartupFundingData(BaseModel):
    id: int
    company_name: str
    country: str
    funding_amount: float
    funding_year: int
    industry: Optional[str]
    stage: Optional[str]
    investors: Optional[str]
    
    class Config:
        from_attributes = True

class RealEstateData(BaseModel):
    id: int
    property_type: str
    location: str
    price: float
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    area_sqft: Optional[int]
    year_built: Optional[int]
    
    class Config:
        from_attributes = True