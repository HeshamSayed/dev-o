# DEV-O Platform

AI-powered development platform with intelligent agents for software development.

## Features

- **AI Chat Interface**: Interactive chat with AI agents for development assistance
- **Project Management**: Create and manage development projects
- **CrewAI Multi-Agent System**: Sequential pipeline of specialized agents (Product Owner, Backend Dev, Frontend Dev, QA Engineer) that generate complete production-ready applications
- **Single-Agent Mode**: Use individual specialized agents for specific tasks
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

## CrewAI Multi-Agent System

DEV-O includes a powerful multi-agent system powered by CrewAI v1.6.1:

- **Sequential Pipeline**: Product Owner → Backend Developer → Frontend Developer → QA Engineer
- **Complete Applications**: Generate fully production-ready applications
- **Real-time Streaming**: Watch agents work in real-time via WebSocket
- **File Management**: All generated files saved to project workspace

See [docs/CREWAI_INTEGRATION.md](docs/CREWAI_INTEGRATION.md) for detailed documentation.

## Production Deployment

The platform is configured for production deployment with:
- SSL/TLS certificates via Certbot
- Nginx reverse proxy
- Production-ready Docker configuration
- Environment-based settings

## License

Proprietary - All rights reserved