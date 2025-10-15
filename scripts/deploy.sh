#!/bin/bash
# scripts/deploy.sh
# Deploy application

set -e

echo "🚀 Deploying Dojo Game Launchpad..."

# Build Docker images
echo "📦 Building Docker images..."
docker-compose -f docker/docker-compose.yml build

# Run database migrations
echo "🔄 Running migrations..."
docker-compose -f docker/docker-compose.yml run --rm api alembic upgrade head

# Start services
echo "▶️  Starting services..."
docker-compose -f docker/docker-compose.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services..."
sleep 10

# Check health
echo "🏥 Checking health..."
curl -f http://localhost:8000/health || exit 1

echo "✅ Deployment complete!"
echo "📊 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
