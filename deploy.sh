#!/bin/bash

# DEV-O Deployment Script
# This script automates the frontend deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Navigate to project root
cd "$(dirname "$0")"

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin master

# Navigate to frontend directory
cd frontend

# Build frontend
echo "🔨 Building frontend..."
VITE_API_URL=https://api.dev-o.ai VITE_WS_URL=wss://api.dev-o.ai npm run build

# Navigate back to project root
cd ..

# Restart nginx to ensure it picks up any changes
echo "🔄 Restarting nginx..."
docker compose restart nginx

# Check if deployment was successful
echo "✅ Checking deployment status..."
sleep 2
if docker ps | grep -q devo_nginx; then
    echo "✅ Deployment successful!"
    echo "🌐 Site is live at https://dev-o.ai"
else
    echo "❌ Deployment failed - nginx is not running"
    exit 1
fi

echo "🎉 Deployment complete!"
