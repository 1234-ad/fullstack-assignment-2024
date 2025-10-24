# Task 3: DataMart SaaS Platform

A mini SaaS platform where users can explore datasets, apply filters, and purchase custom data exports.

## Features

- **Authentication**: JWT-based user registration and login
- **Dataset Explorer**: Browse and filter sample datasets
- **Preview System**: See top 10 matches before purchasing
- **Payment Integration**: Stripe payment processing ($0.05 per row)
- **Data Export**: Download purchased data as CSV
- **User Dashboard**: Track purchases and download history

## Architecture

- **Frontend**: React.js with modern UI
- **Backend**: FastAPI (Python) with async support
- **Database**: PostgreSQL with sample datasets
- **Payment**: Stripe Test Mode integration
- **Containerization**: Docker & Docker Compose

## Sample Datasets

1. **Startup Funding**: Company funding data with filters for country, amount, year
2. **Real Estate**: Property listings with location, price, type filters

## Setup

### With Docker (Recommended)
```bash
docker-compose up --build
```

### Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Database
```bash
# Create PostgreSQL database
createdb datamart
psql datamart < init.sql
```

## Environment Variables

Create `.env` file in backend/:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/datamart
STRIPE_SECRET_KEY=sk_test_your_stripe_key
JWT_SECRET=your_jwt_secret_here
```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Datasets
- `GET /datasets` - List available datasets
- `GET /datasets/{id}` - Get dataset details
- `POST /datasets/{id}/preview` - Preview filtered data
- `POST /datasets/{id}/purchase` - Purchase data rows

### User
- `GET /user/purchases` - Get user purchase history
- `GET /user/downloads/{id}` - Download purchased data

## Payment Flow

1. User applies filters and sees preview (10 rows)
2. User selects number of rows to purchase
3. Stripe payment processing ($0.05 per row)
4. On successful payment, CSV download is generated
5. User can re-download from purchase history

## Database Schema

- `users`: User accounts and authentication
- `datasets`: Available datasets metadata
- `purchases`: User purchase records
- `startup_funding`: Sample startup data
- `real_estate`: Sample property data