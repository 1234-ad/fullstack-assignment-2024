-- Create sample datasets and data for DataMart

-- Insert sample datasets
INSERT INTO datasets (name, description, price_per_row, total_rows, category) VALUES
('Startup Funding Dataset', 'Comprehensive data on startup funding rounds from 2020-2024', 0.05, 5000, 'business'),
('Real Estate Listings', 'Property listings with prices, locations, and features', 0.03, 8000, 'real_estate');

-- Insert sample data for Startup Funding Dataset (dataset_id = 1)
INSERT INTO dataset_rows (dataset_id, data) VALUES
(1, '{"company_name": "TechStart Inc", "funding_amount": 2500000, "country": "India", "year": 2022, "stage": "Series A", "industry": "Technology"}'),
(1, '{"company_name": "GreenEnergy Solutions", "funding_amount": 5000000, "country": "USA", "year": 2023, "stage": "Series B", "industry": "Clean Energy"}'),
(1, '{"company_name": "HealthTech Pro", "funding_amount": 1200000, "country": "India", "year": 2021, "stage": "Seed", "industry": "Healthcare"}'),
(1, '{"company_name": "FinanceAI", "funding_amount": 8000000, "country": "UK", "year": 2023, "stage": "Series C", "industry": "Fintech"}'),
(1, '{"company_name": "EduLearn Platform", "funding_amount": 3200000, "country": "India", "year": 2022, "stage": "Series A", "industry": "Education"}'),
(1, '{"company_name": "FoodDelivery Express", "funding_amount": 15000000, "country": "USA", "year": 2023, "stage": "Series D", "industry": "Food & Beverage"}'),
(1, '{"company_name": "CryptoSecure", "funding_amount": 6500000, "country": "Singapore", "year": 2022, "stage": "Series B", "industry": "Blockchain"}'),
(1, '{"company_name": "AgriTech Solutions", "funding_amount": 4200000, "country": "India", "year": 2021, "stage": "Series A", "industry": "Agriculture"}'),
(1, '{"company_name": "CloudInfra Pro", "funding_amount": 12000000, "country": "USA", "year": 2023, "stage": "Series C", "industry": "Cloud Computing"}'),
(1, '{"company_name": "MobileApp Studio", "funding_amount": 800000, "country": "India", "year": 2020, "stage": "Seed", "industry": "Mobile Apps"}');

-- Insert sample data for Real Estate Dataset (dataset_id = 2)
INSERT INTO dataset_rows (dataset_id, data) VALUES
(2, '{"property_type": "Apartment", "price": 450000, "location": "Mumbai, India", "bedrooms": 2, "bathrooms": 2, "area_sqft": 1200, "year_built": 2018}'),
(2, '{"property_type": "House", "price": 750000, "location": "Bangalore, India", "bedrooms": 3, "bathrooms": 3, "area_sqft": 2000, "year_built": 2020}'),
(2, '{"property_type": "Condo", "price": 320000, "location": "Pune, India", "bedrooms": 1, "bathrooms": 1, "area_sqft": 800, "year_built": 2019}'),
(2, '{"property_type": "Villa", "price": 1200000, "location": "Gurgaon, India", "bedrooms": 4, "bathrooms": 4, "area_sqft": 3500, "year_built": 2021}'),
(2, '{"property_type": "Apartment", "price": 380000, "location": "Chennai, India", "bedrooms": 2, "bathrooms": 2, "area_sqft": 1100, "year_built": 2017}'),
(2, '{"property_type": "House", "price": 650000, "location": "Hyderabad, India", "bedrooms": 3, "bathrooms": 2, "area_sqft": 1800, "year_built": 2019}'),
(2, '{"property_type": "Penthouse", "price": 2500000, "location": "Mumbai, India", "bedrooms": 4, "bathrooms": 5, "area_sqft": 4000, "year_built": 2022}'),
(2, '{"property_type": "Studio", "price": 250000, "location": "Kolkata, India", "bedrooms": 1, "bathrooms": 1, "area_sqft": 600, "year_built": 2018}'),
(2, '{"property_type": "Duplex", "price": 950000, "location": "Delhi, India", "bedrooms": 3, "bathrooms": 3, "area_sqft": 2500, "year_built": 2020}'),
(2, '{"property_type": "Apartment", "price": 420000, "location": "Ahmedabad, India", "bedrooms": 2, "bathrooms": 2, "area_sqft": 1300, "year_built": 2019}');

-- Add more sample data to reach meaningful dataset sizes
-- (In a real application, you would have thousands of rows)
-- This is just for demonstration purposes