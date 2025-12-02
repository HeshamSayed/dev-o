# DEV-O Platform

AI-powered development platform with intelligent agents for software development.

## Features

- **AI Chat Interface**: Interactive chat with AI agents for development assistance
- **Project Management**: Create and manage development projects
- **Multi-Agent System**: Specialized agents for different development tasks
- **Referral Program**: Share DEV-O with friends and earn bonus quotas
- **Subscription Plans**: Flexible pricing with free and paid tiers

## Technology Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Web Server**: Nginx
- **Containerization**: Docker

## Quick Start

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

## Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `STRIPE_SECRET_KEY`: Stripe key for payments
- `FRONTEND_URL`: Production frontend URL

## Services

- **Frontend**: https://chat.dev-o.ai
- **Backend API**: https://api.dev-o.ai
- **Admin Panel**: https://api.dev-o.ai/admin

## Development

```bash
# Build frontend
cd frontend
npm install
npm run build

# Backend migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## Production Deployment

The platform is configured for production deployment with:
- SSL/TLS certificates via Certbot
- Nginx reverse proxy
- Production-ready Docker configuration
- Environment-based settings

## License

Proprietary - All rights reserved