# Deployment Guide - AI Inference Service

Complete guide for deploying the Mistral 7B inference service to production server `34.136.165.200:7000`.

## Prerequisites

### On Deployment Server (34.136.165.200)

1. **NVIDIA GPU with CUDA support**
   ```bash
   # Check GPU
   nvidia-smi
   
   # Should show GPU details and CUDA version
   ```

2. **Docker and nvidia-docker**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install nvidia-docker
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
     sudo tee /etc/os-release.list
   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

3. **Sufficient disk space**
   - Model cache: ~14GB
   - Docker images: ~10GB
   - Total recommended: 30GB+ free space

## Deployment Steps

### 1. Clone Repository

```bash
ssh user@34.136.165.200
cd /opt
git clone https://github.com/HeshamSayed/dev-o.git
cd dev-o/inference_service
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Recommended production settings:
```bash
HOST=0.0.0.0
PORT=7000
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
DEVICE=cuda
MAX_INPUT_TOKENS=4096
MAX_OUTPUT_TOKENS=2048

# Enable quantization if VRAM < 14GB
LOAD_IN_4BIT=false
LOAD_IN_8BIT=false

# Optional: Add API key for security
# API_KEY=your-secret-production-key
```

### 3. Build and Start Service

```bash
# Build Docker image (first time only, ~10 minutes)
docker-compose build

# Start service
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Verify Deployment

```bash
# Check service health
curl http://localhost:7000/health

# Expected response:
# {"status":"healthy","model_loaded":true,"model_name":"...","device":"cuda"}

# Test from external machine
curl http://34.136.165.200:7000/health
```

### 5. Test API Endpoints

```bash
# Test chat completion
curl -X POST http://localhost:7000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'

# Test text completion
curl -X POST http://localhost:7000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b",
    "prompt": "Python code to sort a list:",
    "max_tokens": 100
  }'
```

## Firewall Configuration

```bash
# Allow port 7000
sudo ufw allow 7000/tcp

# Check firewall status
sudo ufw status
```

## Monitoring

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service logs
docker logs mistral-inference-service
```

### Check Resource Usage

```bash
# GPU usage
nvidia-smi

# Docker stats
docker stats mistral-inference-service

# Disk usage
df -h
du -sh /root/.cache/huggingface
```

### Health Monitoring

```bash
# Manual health check
curl http://localhost:7000/health

# Set up automated monitoring (optional)
# Add to crontab:
*/5 * * * * curl -f http://localhost:7000/health || systemctl restart docker
```

## Maintenance

### Update Service

```bash
cd /opt/dev-o
git pull origin main
cd inference_service
docker-compose down
docker-compose build
docker-compose up -d
```

### Restart Service

```bash
docker-compose restart
```

### Stop Service

```bash
docker-compose down
```

### Clear Cache (if needed)

```bash
# Stop service first
docker-compose down

# Clear model cache
sudo rm -rf /root/.cache/huggingface

# Restart
docker-compose up -d
```

## Performance Tuning

### Optimize for Low VRAM

Edit `.env`:
```bash
# Use 4-bit quantization for ~4GB VRAM
LOAD_IN_4BIT=true

# Or 8-bit for ~7GB VRAM
LOAD_IN_8BIT=true
```

Restart after changes:
```bash
docker-compose restart
```

### Adjust Token Limits

For faster responses, reduce max tokens:
```bash
MAX_OUTPUT_TOKENS=1024  # Instead of 2048
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs for errors
docker-compose logs

# Common issues:
# 1. Out of memory - enable quantization
# 2. CUDA not available - install nvidia-docker
# 3. Port in use - check: sudo lsof -i :7000
```

### Model Loading Takes Too Long

- First startup downloads ~14GB model (can take 30+ minutes)
- Subsequent starts are faster (~2 minutes)
- Model is cached in `/root/.cache/huggingface`

### Out of Memory Errors

```bash
# Enable quantization
nano .env
# Set LOAD_IN_4BIT=true

docker-compose restart
```

### API Returns 503 Errors

```bash
# Check if model is loaded
curl http://localhost:7000/health

# If model_loaded=false, check logs
docker-compose logs -f
```

## Integration with DEV-O

Once deployed, configure DEV-O backend:

```bash
# In DEV-O's .env file:
AI_SERVICE_URL=http://34.136.165.200:7000
AI_SERVICE_MODEL=mistral-7b
AI_SERVICE_TIMEOUT=120
```

## Security Recommendations

1. **Enable API Key Authentication**
   ```bash
   # In .env
   API_KEY=your-strong-secret-key-here
   ```

2. **Use Firewall Rules**
   ```bash
   # Only allow DEV-O server IP
   sudo ufw allow from <devo-server-ip> to any port 7000
   ```

3. **Set up HTTPS** (optional)
   - Use nginx as reverse proxy
   - Configure SSL certificates
   - Forward requests to localhost:7000

## Backup

```bash
# Backup configuration
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup

# Backup model cache (optional, large)
tar -czf model-cache-backup.tar.gz /root/.cache/huggingface
```

## Support

For issues specific to:
- **Model loading**: Check HuggingFace transformers documentation
- **CUDA errors**: Verify nvidia-docker and CUDA compatibility
- **API integration**: See DEV-O's `docs/AI_INFERENCE_SERVICE.md`

## Production Checklist

- [ ] GPU available and detected
- [ ] Docker and nvidia-docker installed
- [ ] Sufficient disk space (30GB+)
- [ ] Environment variables configured
- [ ] Service built and started
- [ ] Health endpoint returns healthy
- [ ] API endpoints tested
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] DEV-O integration tested

## Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Health
curl http://localhost:7000/health

# Update
git pull && docker-compose build && docker-compose restart
```
