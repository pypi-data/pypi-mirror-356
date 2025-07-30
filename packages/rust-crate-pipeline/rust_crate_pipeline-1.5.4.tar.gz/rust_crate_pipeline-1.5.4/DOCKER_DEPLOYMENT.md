# Docker Deployment Guide for SigilDERG-Data_Production v1.5.1

## Overview

This guide covers deploying SigilDERG-Data_Production v1.5.1 using Docker with full Crawl4AI integration and GGUF model support.

## Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+
- At least 8GB RAM available for the container
- 4 CPU cores recommended
- GGUF model file: `deepseek-coder-6.7b-instruct.Q4_K_M.gguf`

## Model Setup

### Local Model Directory
```bash
# Create local models directory
mkdir -p ~/models/deepseek

# Download the GGUF model (example)
wget -O ~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf \
  "https://example.com/path/to/model"
```

### Windows Model Directory
```powershell
# Create local models directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\models\deepseek"

# Place your GGUF model file in:
# %USERPROFILE%\models\deepseek\deepseek-coder-6.7b-instruct.Q4_K_M.gguf
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# GitHub API Token (optional but recommended)
GITHUB_TOKEN=your_github_token_here

# Logging configuration
LOG_LEVEL=INFO

# Model configuration (GGUF with llama-cpp-python)  
MODEL_PATH=/app/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf
LLM_MODEL_PATH=/app/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf
CRAWL4AI_MODEL=/app/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf

# LLM inference parameters
LLM_CONTEXT_SIZE=4096
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.1

# Host model directory (adjust path as needed)
# Linux/Mac: HOME=/home/username or /Users/username
# Windows: HOME=C:/Users/username
HOME=/path/to/your/home/directory
```

## Deployment Methods

### Method 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Superuser666-Sigil/SigilDERG-Data_Production.git
cd SigilDERG-Data_Production

# Create required directories
mkdir -p output logs cache data

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f rust-crate-pipeline

# Stop the service
docker-compose down
```

### Method 2: Docker Build and Run

```bash
# Build the image
docker build -t rust-crate-pipeline:1.5.1 .

# Run the container
docker run -d \
  --name rust-pipeline \
  --restart unless-stopped \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/cache:/app/cache \
  -v ~/models:/app/models:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  -e LOG_LEVEL=INFO \
  rust-crate-pipeline:1.5.1 \
  --limit 1000 --batch-size 10
```

## Container Management

### Interactive Shell Access
```bash
# Access running container
docker exec -it rust-pipeline bash

# Or start in interactive mode
docker run -it --rm rust-crate-pipeline:1.5.1 bash
```

### Health Check
```bash
# Check container health
docker ps
docker inspect rust-pipeline | grep -A 10 Health

# Manual health check
docker exec rust-pipeline python -c "
import rust_crate_pipeline
from rust_crate_pipeline.config import PipelineConfig
PipelineConfig()
print('✅ Container health check passed')
"
```

### Container Testing
```bash
# Run container test mode
docker run --rm rust-crate-pipeline:1.5.1 test
```

## Configuration Validation

### Verify Model Paths
```bash
docker exec rust-pipeline ls -la /app/models/deepseek/
docker exec rust-pipeline python -c "
import os
model_path = os.environ.get('LLM_MODEL_PATH')
print(f'Model path: {model_path}')
print(f'Model exists: {os.path.exists(model_path) if model_path else False}')
"
```

### Verify Crawl4AI Integration
```bash
docker exec rust-pipeline python -c "
import crawl4ai
from crawl4ai import AsyncWebCrawler
print('✅ Crawl4AI available')
print(f'Chromium path: /usr/bin/chromium')
import os
print(f'Chromium exists: {os.path.exists(\"/usr/bin/chromium\")}')
"
```

## Log Monitoring

### Using Docker Logs
```bash
# Follow logs
docker logs -f rust-pipeline

# View recent logs
docker logs --tail 100 rust-pipeline
```

### Using Dozzle (Web UI)
```bash
# Start with monitoring profile
docker-compose --profile monitoring up -d

# Access logs at http://localhost:8081
```

## Performance Tuning

### Resource Limits
The default configuration allocates:
- **CPU**: 4 cores limit, 2 cores reserved
- **Memory**: 8GB limit, 4GB reserved

Adjust in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '6.0'        # Increase for better performance
      memory: 12G        # Increase for larger models
    reservations:
      cpus: '3.0'
      memory: 6G
```

### Model Optimization
- Use GGUF models for better memory efficiency
- Adjust `LLM_CONTEXT_SIZE` based on available memory
- Lower `LLM_TEMPERATURE` for more deterministic results

## Troubleshooting

### Common Issues

1. **Model not found**
   ```bash
   # Check model mount and permissions
   docker exec rust-pipeline ls -la /app/models/deepseek/
   docker exec rust-pipeline cat /proc/mounts | grep models
   ```

2. **Memory issues**
   ```bash
   # Check container memory usage
   docker stats rust-pipeline
   
   # Reduce model context size
   docker exec rust-pipeline python -c "
   import os
   print(f'Context size: {os.environ.get(\"LLM_CONTEXT_SIZE\", \"default\")}')
   "
   ```

3. **Crawl4AI browser issues**
   ```bash
   # Check browser installation
   docker exec rust-pipeline /usr/bin/chromium --version
   docker exec rust-pipeline python -m playwright install --help
   ```

### Debug Mode
```bash
# Run with debug logging
docker run --rm \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/output:/app/output \
  -v ~/models:/app/models:ro \
  rust-crate-pipeline:1.5.1 \
  --limit 10 --log-level DEBUG
```

## Security Considerations

1. **Non-root user**: Container runs as `pipelineuser` (UID 1000)
2. **Read-only model mount**: Models are mounted read-only
3. **No user site-packages**: `PYTHONNOUSERSITE=1` prevents loading user packages
4. **Hash randomization**: `PYTHONHASHSEED=random` for security

## Production Recommendations

1. **Use specific tags**: Pin to `rust-crate-pipeline:1.5.1` instead of `latest`
2. **Resource monitoring**: Use proper monitoring for CPU/memory usage
3. **Log rotation**: Configure log rotation for long-running containers
4. **Health checks**: Monitor container health endpoints
5. **Security updates**: Regularly update base images

## Version Information

- **Image Version**: 1.5.1
- **Base Image**: python:3.11.9-slim-bookworm
- **Python Version**: 3.11.9
- **Crawl4AI**: Latest compatible version
- **Model Format**: GGUF (llama-cpp-python compatible)

## Support

For issues or questions:
- GitHub Issues: https://github.com/Superuser666-Sigil/SigilDERG-Data_Production/issues
- Documentation: https://github.com/Superuser666-Sigil/SigilDERG-Data_Production/blob/main/README.md
