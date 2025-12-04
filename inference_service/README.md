# AI Inference Service - Mistral 7B

Production-ready FastAPI application providing OpenAI-compatible API endpoints for Mistral 7B model inference.

## Features

✅ **OpenAI-Compatible API** - Drop-in replacement for OpenAI endpoints  
✅ **Token Limits Enforced** - 4096 input, 2048 output tokens  
✅ **GPU Acceleration** - CUDA support with automatic device management  
✅ **Memory Optimization** - Optional 4-bit/8-bit quantization  
✅ **Docker Support** - nvidia-docker for easy deployment  
✅ **Health Monitoring** - Automatic health checks and restart policies  

## Quick Start

### Prerequisites

- Python 3.10+
- NVIDIA GPU with CUDA 12.1+ (recommended)
- 14GB+ VRAM (or 4GB+ with quantization)

### Installation

```bash
# Clone repository
cd inference_service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### Running Locally

```bash
python run.py
```

Service will start at `http://localhost:7000`

### Running with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "mistralai/Mistral-7B-Instruct-v0.2",
  "device": "cuda"
}
```

### Chat Completions

```bash
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "mistral-7b",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

### Text Completions

```bash
POST /v1/completions
Content-Type: application/json

{
  "model": "mistral-7b",
  "prompt": "Once upon a time",
  "temperature": 0.7,
  "max_tokens": 500
}
```

## Configuration

Environment variables (`.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| HOST | 0.0.0.0 | Server host |
| PORT | 7000 | Server port |
| MODEL_NAME | mistralai/Mistral-7B-Instruct-v0.2 | HuggingFace model |
| DEVICE | cuda | Device (cuda/cpu) |
| MAX_INPUT_TOKENS | 4096 | Maximum input tokens |
| MAX_OUTPUT_TOKENS | 2048 | Maximum output tokens |
| LOAD_IN_4BIT | false | Enable 4-bit quantization (~4GB VRAM) |
| LOAD_IN_8BIT | false | Enable 8-bit quantization (~7GB VRAM) |
| API_KEY | - | Optional API key for authentication |

## Memory Requirements

| Configuration | VRAM | Quality |
|--------------|------|---------|
| Full Precision (FP16) | ~14 GB | Best |
| 8-bit Quantization | ~7 GB | Good |
| 4-bit Quantization | ~4 GB | Acceptable |

To enable quantization, set `LOAD_IN_4BIT=true` or `LOAD_IN_8BIT=true` in `.env`

## Testing

```bash
# Start the service first
python run.py

# In another terminal, run tests
python test_service.py
```

## Integration with DEV-O

This service is designed to work with the DEV-O CrewAI system. Configure DEV-O with:

```bash
AI_SERVICE_URL=http://34.136.165.200:7000
AI_SERVICE_MODEL=mistral-7b
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions to 34.136.165.200:7000.

## Troubleshooting

**Model loading fails:**
- Check CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
- Try enabling quantization to reduce memory
- Check disk space for model cache (~14GB)

**Out of memory errors:**
- Enable 4-bit or 8-bit quantization in `.env`
- Reduce `MAX_OUTPUT_TOKENS`
- Use a GPU with more VRAM

**Service not responding:**
- Check logs: `docker-compose logs -f`
- Verify model loaded: `curl http://localhost:7000/health`
- Check firewall allows port 7000

## License

This service is part of the DEV-O project.
