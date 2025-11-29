#!/bin/bash

# DEVO Backend Setup Script
# This script sets up the development environment for the DEVO backend

set -e  # Exit on error

echo "======================================"
echo "DEVO Backend Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env with your configuration"
fi

# Check PostgreSQL connection
echo ""
echo "Checking PostgreSQL connection..."
if command -v psql &> /dev/null; then
    echo "✓ PostgreSQL is installed"
else
    echo "⚠️  PostgreSQL is not installed or not in PATH"
    echo "   Please install PostgreSQL 15+ with pgvector extension"
fi

# Check Redis connection
echo ""
echo "Checking Redis connection..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✓ Redis is running"
    else
        echo "⚠️  Redis is not running"
        echo "   Please start Redis: redis-server"
    fi
else
    echo "⚠️  Redis is not installed or not in PATH"
    echo "   Please install Redis 7.0+"
fi

# Run migrations
echo ""
read -p "Do you want to run database migrations? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating migrations..."
    python manage.py makemigrations
    echo ""
    echo "Running migrations..."
    python manage.py migrate
    echo "✓ Migrations completed"
fi

# Create superuser
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run the development server: python manage.py runserver"
echo "3. Access the admin at: http://localhost:8000/admin"
echo "4. Access the API at: http://localhost:8000/api/"
echo ""
echo "For more information, see README.md"
echo ""
