#!/bin/bash
# scripts/init_db.sh
# Initialize database

set -e

echo "🔧 Initializing Database..."

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running"
    echo "Start with: docker-compose up -d postgres"
    exit 1
fi

# Run initialization
python backend/deploy.py init

echo "✅ Database initialization complete!"
