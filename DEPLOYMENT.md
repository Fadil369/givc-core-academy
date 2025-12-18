# GIVC Core Academy - Deployment Guide

## Quick Start (Development)

### Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Fadil369/givc-core-academy.git
cd givc-core-academy

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Access the services
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/api/docs
# - Frontend: http://localhost:3000
```

## Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="sqlite:///./givc_academy.db"
export SECRET_KEY="your-secret-key"

# Initialize database
python scripts/seed_data.py

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

### Mobile Setup

```bash
cd mobile

# Install dependencies
npm install

# Start Expo
npm start
```

## Production Deployment

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application
DEBUG=false

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_HOST=redis-host
REDIS_PORT=6379

# Security (MUST CHANGE)
SECRET_KEY=your-secure-random-secret-key

# Stripe
STRIPE_API_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Backend Production

```bash
cd backend

# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend Production

```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start
```

### Docker Production

```bash
# Build images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Database Migrations

### Creating Migrations

```bash
cd backend

# Install alembic (already in requirements.txt)
pip install alembic

# Initialize alembic (if not done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Monitoring

### Health Check Endpoints

- Backend: `GET /health`
- Response: `{"status": "healthy", "app_name": "GIVC Core Academy", "version": "1.0.0"}`

### Logs

```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery_worker
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Performance Optimization

### Backend

1. **Database Connection Pooling**: Already configured in SQLAlchemy
2. **Redis Caching**: Use for frequently accessed data
3. **Celery Tasks**: Offload heavy processing to background tasks

### Frontend

1. **Next.js Static Generation**: Use ISR for course catalog pages
2. **Image Optimization**: Use Next.js Image component
3. **Code Splitting**: Automatic with Next.js App Router

## Security Checklist

- [x] SECRET_KEY must be set in production (enforced)
- [x] HTTPS/TLS 1.3 for all communications
- [x] JWT tokens with expiration
- [x] MFA support for privileged roles
- [x] Rate limiting on API endpoints
- [x] Input validation with Pydantic
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS prevention (React auto-escaping)
- [x] CORS properly configured
- [x] No security vulnerabilities (CodeQL verified)

## Backup Strategy

### Database Backup

```bash
# PostgreSQL backup
pg_dump -U givc -h localhost givc_academy > backup_$(date +%Y%m%d).sql

# Restore
psql -U givc -h localhost givc_academy < backup_20231218.sql
```

### Redis Backup

Redis persistence is configured in docker-compose.yml with RDB snapshots.

## Scaling

### Horizontal Scaling

1. **Backend**: Run multiple instances behind a load balancer
2. **Celery Workers**: Scale workers based on queue length
3. **Database**: Use read replicas for read-heavy operations

### Vertical Scaling

1. **Database**: Increase PostgreSQL resources (CPU, RAM)
2. **Redis**: Use Redis Cluster for larger datasets

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Database not ready: Wait for health check
# - Missing SECRET_KEY: Set in .env file
# - Port already in use: Change port in docker-compose.yml
```

### Frontend Build Fails

```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### Database Connection Issues

```bash
# Test connection
docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/Fadil369/givc-core-academy/issues
- Email: support@givc.sa
- Documentation: http://localhost:8000/api/docs
