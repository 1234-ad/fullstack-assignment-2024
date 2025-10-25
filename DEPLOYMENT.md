# Deployment Guide

This guide provides instructions for deploying the DataMart SaaS platform (Task 3) to various cloud platforms.

## Prerequisites

- GitHub account
- Stripe account (for payment processing)
- PostgreSQL database (provided by hosting platform or external service)

## Option 1: Deploy to Render (Recommended)

### Backend Deployment

1. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `datamart-backend`
     - **Root Directory**: `task3-datamart/backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Add Environment Variables**:
   ```
   DATABASE_URL=<your-postgres-connection-string>
   STRIPE_SECRET_KEY=<your-stripe-test-key>
   JWT_SECRET=<generate-random-secret>
   PYTHON_VERSION=3.11.0
   ```

3. **Create PostgreSQL Database**
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - Name it `datamart-db`
   - Copy the Internal Database URL
   - Use this URL for `DATABASE_URL` in backend environment variables

4. **Initialize Database**
   - After deployment, connect to your database
   - Run the SQL scripts:
     - `task3-datamart/backend/init.sql`
     - `task3-datamart/backend/additional_data.sql`

### Frontend Deployment

1. **Create a new Static Site on Render**
   - Click "New +" → "Static Site"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `datamart-frontend`
     - **Root Directory**: `task3-datamart/frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `build`

2. **Add Environment Variable**:
   ```
   REACT_APP_API_URL=<your-backend-url>
   ```
   (Use the backend URL from step 1)

---

## Option 2: Deploy to Railway

### Backend

1. **Create New Project**
   - Go to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Backend Service**
   - Add service from `task3-datamart/backend`
   - Railway will auto-detect Python
   - Add environment variables (same as Render)

3. **Add PostgreSQL**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

### Frontend

1. **Add Frontend Service**
   - Click "New" → "GitHub Repo"
   - Set root directory to `task3-datamart/frontend`
   - Add `REACT_APP_API_URL` environment variable

---

## Option 3: Deploy to Vercel (Frontend) + Render (Backend)

### Backend on Render
Follow the Render backend instructions above.

### Frontend on Vercel

1. **Import Project**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository

2. **Configure**
   - **Root Directory**: `task3-datamart/frontend`
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

3. **Environment Variables**:
   ```
   REACT_APP_API_URL=<your-render-backend-url>
   ```

---

## Option 4: Deploy Task 2 (Site Generator)

### Backend (Render/Railway)
- **Root Directory**: `task2-site-generator/backend`
- **Build Command**: `npm install`
- **Start Command**: `node server.js`
- **Port**: 3001

### Frontend (Vercel/Netlify)
- **Root Directory**: `task2-site-generator/frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Environment Variable**: `REACT_APP_API_URL=<backend-url>`

---

## Post-Deployment Checklist

- [ ] Backend is accessible and returns health check
- [ ] Frontend loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Dataset preview displays correctly
- [ ] Stripe payment integration works (test mode)
- [ ] CSV download works after purchase
- [ ] CORS is properly configured
- [ ] Environment variables are set correctly
- [ ] Database is initialized with sample data

---

## Troubleshooting

### CORS Errors
Ensure backend CORS middleware includes your frontend URL:
```python
allow_origins=["https://your-frontend-url.com"]
```

### Database Connection Issues
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Ensure database is initialized with schema
- Check if database accepts external connections

### Stripe Payment Fails
- Verify `STRIPE_SECRET_KEY` starts with `sk_test_`
- Check Stripe dashboard for test mode
- Ensure webhook endpoints are configured (if using webhooks)

### Build Failures
- Check Node.js version (use 18.x)
- Check Python version (use 3.11)
- Verify all dependencies are in requirements.txt/package.json

---

## Environment Variables Reference

### Backend (Task 3)
```
DATABASE_URL=postgresql://user:password@host:port/database
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
JWT_SECRET=your-random-secret-key-here
PYTHON_VERSION=3.11.0
```

### Frontend (Task 3)
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Backend (Task 2)
```
NODE_ENV=production
PORT=3001
```

### Frontend (Task 2)
```
REACT_APP_API_URL=https://your-backend-url.com
```

---

## Quick Deploy Commands

### Using Render CLI
```bash
# Install Render CLI
npm install -g @render/cli

# Deploy backend
render deploy --service datamart-backend

# Deploy frontend
render deploy --service datamart-frontend
```

### Using Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

---

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Verify environment variables
4. Test database connectivity
5. Check CORS configuration

---

## Production Considerations

Before going to production:
- [ ] Switch Stripe to live mode
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure monitoring
- [ ] Set up automated backups
- [ ] Review security settings
- [ ] Add rate limiting
- [ ] Configure CDN for static assets
- [ ] Set up CI/CD pipeline
