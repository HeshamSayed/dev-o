# DEV-O LLM Inference Service

This branch contains **only** the LLM inference service for DEV-O platform.

## What's Here

This repository contains a standalone FastAPI service for running Mistral 7B model inference:

```
inference_service/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── model_loader.py  # Model loading logic
│   └── models.py        # Pydantic models
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── requirements.txt     # Python dependencies
├── README.md           # Service documentation
├── DEPLOYMENT.md       # Deployment guide
└── test_service.py     # Service tests
```

## Quick Start

```bash
cd inference_service
docker-compose up -d
```

The service will be available at `http://localhost:7000`

## Documentation

See [inference_service/README.md](inference_service/README.md) for detailed documentation.

## Main DEV-O Platform

For the complete DEV-O platform with CrewAI multi-agent system, see the `master` branch:
- [Master Branch](https://github.com/HeshamSayed/dev-o/tree/master)

## About

This inference service provides:
- Mistral 7B model hosting
- OpenAI-compatible API endpoints
- GPU acceleration support
- Docker deployment

Part of the DEV-O AI-powered development platform.
