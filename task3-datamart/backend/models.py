from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    purchases = relationship("Purchase", back_populates="user")

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    table_name = Column(String, nullable=False)
    price_per_row = Column(Float, default=0.05)
    total_rows = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    purchases = relationship("Purchase", back_populates="dataset")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    rows_purchased = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    stripe_payment_id = Column(String)
    filters_applied = Column(Text)  # JSON string of filters
    created_at = Column(DateTime, default=datetime.utcnow)
    download_url = Column(String)
    
    user = relationship("User", back_populates="purchases")
    dataset = relationship("Dataset", back_populates="purchases")

class StartupFunding(Base):
    __tablename__ = "startup_funding"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    funding_amount = Column(Float, nullable=False)
    funding_year = Column(Integer, nullable=False)
    industry = Column(String)
    stage = Column(String)
    investors = Column(String)

class RealEstate(Base):
    __tablename__ = "real_estate"
    
    id = Column(Integer, primary_key=True, index=True)
    property_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Integer)
    year_built = Column(Integer)