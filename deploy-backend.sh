#!/bin/bash

# DEV-O Backend Deployment Script
# This script automates the backend deployment process

set -e  # Exit on any error

echo "🚀 Starting backend deployment..."

# Navigate to project root
cd "$(dirname "$0")"

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin master

# Check if requirements.txt changed
echo "🔍 Checking for dependency changes..."
REQUIREMENTS_CHANGED=$(git diff HEAD@{1} HEAD --name-only | grep -c "backend/requirements.txt" || echo "0")

if [ "$REQUIREMENTS_CHANGED" -gt 0 ]; then
    echo "📦 Dependencies changed - rebuilding backend container..."
    docker compose build backend celery
else
    echo "✅ No dependency changes detected"
fi

# Run database migrations
echo "🗄️  Running database migrations..."
docker compose exec backend python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker compose exec backend python manage.py collectstatic --noinput

# Restart backend services
echo "🔄 Restarting backend services..."
docker compose restart backend celery

# Check if services are running
echo "✅ Checking service status..."
sleep 3

if docker ps | grep -q devo_backend && docker ps | grep -q devo_celery; then
    echo "✅ Backend deployment successful!"
    echo "🌐 API is live at https://api.dev-o.ai"

    # Show recent logs
    echo ""
    echo "📋 Recent backend logs:"
    docker compose logs --tail=20 backend
else
    echo "❌ Backend deployment failed - services not running"
    docker compose ps
    exit 1
fi

echo "🎉 Backend deployment complete!"
