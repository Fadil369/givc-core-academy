#!/bin/bash

echo "Setting up GIVC Core Academy Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Application
DEBUG=true

# Database
POSTGRES_SERVER=postgres
POSTGRES_USER=givc
POSTGRES_PASSWORD=givc123
POSTGRES_DB=givc_academy
DATABASE_URL=postgresql://givc:givc123@postgres:5432/givc_academy

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Security
SECRET_KEY=$(openssl rand -hex 32)

# Stripe (add your keys)
STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo ".env file created successfully"
fi

# Build and start services
echo "Building and starting Docker containers..."
docker-compose up --build -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "Services running:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/api/docs"
echo "  - Frontend: http://localhost:3000"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
