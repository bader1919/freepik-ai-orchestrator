# Docker Deployment Guide

This guide provides comprehensive instructions for deploying the Freepik AI Orchestrator using Docker in various environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Images](#docker-images)
- [Environment Configuration](#environment-configuration)
- [Single Container Deployment](#single-container-deployment)
- [Multi-Container Deployment](#multi-container-deployment)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Docker Compose Examples](#docker-compose-examples)
- [Scaling and Load Balancing](#scaling-and-load-balancing)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker 20.10 or higher
- Docker Compose 2.0 or higher
- At least 4GB RAM available
- Valid API keys for AI services

### Run with Docker Compose

```bash
# Clone repository
git clone https://github.com/freepik/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env

# Start services
docker-compose up -d

# Access application
open http://localhost:8501
```

## Docker Images

### Official Images

The project provides pre-built Docker images:

```bash
# Pull latest image
docker pull freepik/ai-orchestrator:latest

# Pull specific version
docker pull freepik/ai-orchestrator:v1.2.0

# Pull development image
docker pull freepik/ai-orchestrator:develop
```

### Image Variants

| Tag | Description | Size | Use Case |
|-----|-------------|------|----------|
| `latest` | Latest stable release | ~800MB | Production |
| `v1.x.x` | Specific version | ~800MB | Production |
| `develop` | Development build | ~900MB | Testing |
| `slim` | Minimal dependencies | ~400MB | Resource-constrained |
| `gpu` | CUDA support | ~2GB | GPU acceleration |

### Building Custom Images

```bash
# Build standard image
docker build -t freepik-ai-orchestrator .

# Build with custom tag
docker build -t freepik-ai-orchestrator:custom .

# Build development image
docker build -f Dockerfile.dev -t freepik-ai-orchestrator:dev .

# Build GPU-enabled image
docker build -f Dockerfile.gpu -t freepik-ai-orchestrator:gpu .
```

## Environment Configuration

### Environment Variables

Create a `.env` file with required configuration:

```env
# Application Settings
APP_NAME=Freepik AI Orchestrator
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# API Keys
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
STABILITY_API_KEY=sk-your-stability-key

# Database Configuration
DATABASE_URL=postgresql://user:password@postgres:5432/orchestrator
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# External Services
WEBHOOK_URL=https://your-domain.com/webhooks
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=your-bucket-name

# Performance
MAX_WORKERS=4
CACHE_TTL=3600
REQUEST_TIMEOUT=300
```

### Docker Environment Variables

```bash
# Set environment variables for Docker
export COMPOSE_PROJECT_NAME=freepik-orchestrator
export COMPOSE_FILE=docker-compose.yml
export DOCKER_BUILDKIT=1
```

## Single Container Deployment

### Basic Deployment

```bash
# Run single container
docker run -d \
  --name ai-orchestrator \
  -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-key \
  -e DATABASE_URL=sqlite:///app/data/orchestrator.db \
  -v $(pwd)/data:/app/data \
  freepik/ai-orchestrator:latest
```

### With Persistent Storage

```bash
# Create volume for persistent data
docker volume create orchestrator-data

# Run with persistent storage
docker run -d \
  --name ai-orchestrator \
  -p 8501:8501 \
  --env-file .env \
  -v orchestrator-data:/app/data \
  -v $(pwd)/logs:/app/logs \
  freepik/ai-orchestrator:latest
```

### With GPU Support

```bash
# Run with GPU acceleration
docker run -d \
  --name ai-orchestrator-gpu \
  --gpus all \
  -p 8501:8501 \
  --env-file .env \
  -v orchestrator-data:/app/data \
  freepik/ai-orchestrator:gpu
```

## Multi-Container Deployment

### Basic Docker Compose

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    image: freepik/ai-orchestrator:latest
    container_name: ai-orchestrator
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/orchestrator
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - orchestrator-network

  postgres:
    image: postgres:15
    container_name: ai-orchestrator-db
    environment:
      POSTGRES_DB: orchestrator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    networks:
      - orchestrator-network

  redis:
    image: redis:7-alpine
    container_name: ai-orchestrator-cache
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - orchestrator-network

  nginx:
    image: nginx:alpine
    container_name: ai-orchestrator-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - orchestrator-network

volumes:
  app-data:
  postgres-data:
  redis-data:

networks:
  orchestrator-network:
    driver: bridge
```

### Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale application
docker-compose up -d --scale app=3

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## Development Setup

### Development Docker Compose

**docker-compose.dev.yml:**

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: ai-orchestrator-dev
    ports:
      - "8501:8501"
      - "8000:8000"  # API port
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
      - RELOAD=true
    env_file:
      - .env.dev
    volumes:
      - .:/app
      - /app/node_modules
      - dev-data:/app/data
    depends_on:
      - postgres-dev
      - redis-dev
    restart: unless-stopped
    networks:
      - dev-network

  postgres-dev:
    image: postgres:15
    container_name: ai-orchestrator-db-dev
    environment:
      POSTGRES_DB: orchestrator_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5433:5432"
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data
    networks:
      - dev-network

  redis-dev:
    image: redis:7-alpine
    container_name: ai-orchestrator-cache-dev
    ports:
      - "6380:6379"
    volumes:
      - redis-dev-data:/data
    networks:
      - dev-network

  mailhog:
    image: mailhog/mailhog
    container_name: ai-orchestrator-mail-dev
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - dev-network

volumes:
  dev-data:
  postgres-dev-data:
  redis-dev-data:

networks:
  dev-network:
    driver: bridge
```

### Development Commands

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Watch logs
docker-compose -f docker-compose.dev.yml logs -f app

# Execute commands in container
docker-compose -f docker-compose.dev.yml exec app bash
docker-compose -f docker-compose.dev.yml exec app python manage.py migrate

# Run tests
docker-compose -f docker-compose.dev.yml exec app pytest

# Access database
docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U postgres -d orchestrator_dev
```

## Production Deployment

### Production Docker Compose

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
  app:
    image: freepik/ai-orchestrator:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/orchestrator
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=false
      - LOG_LEVEL=INFO
    env_file:
      - .env.prod
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
    networks:
      - prod-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: orchestrator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - prod-network
    deploy:
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - prod-network
    deploy:
      restart_policy:
        condition: on-failure

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - ./static:/var/www/static
    depends_on:
      - app
    networks:
      - prod-network
    deploy:
      restart_policy:
        condition: on-failure

  backup:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./backups:/backups
      - ./backup-scripts:/scripts
    command: /scripts/backup.sh
    networks:
      - prod-network
    deploy:
      restart_policy:
        condition: on-failure

volumes:
  app-data:
  postgres-data:
  redis-data:

networks:
  prod-network:
    driver: overlay
    encrypted: true

secrets:
  postgres_password:
    external: true
  redis_password:
    external: true
```

### Production Commands

```bash
# Deploy to production
docker stack deploy -c docker-compose.prod.yml orchestrator

# Update service
docker service update --image freepik/ai-orchestrator:v1.2.0 orchestrator_app

# Scale service
docker service scale orchestrator_app=5

# View service status
docker service ls
docker service ps orchestrator_app

# View logs
docker service logs -f orchestrator_app
```

## Docker Compose Examples

### Minimal Setup

```yaml
version: '3.8'
services:
  app:
    image: freepik/ai-orchestrator:latest
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
```

### With Monitoring

```yaml
version: '3.8'
services:
  app:
    image: freepik/ai-orchestrator:latest
    ports:
      - "8501:8501"
    env_file: .env
    depends_on:
      - postgres
      - redis
    
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: orchestrator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  postgres-data:
  redis-data:
  grafana-data:
```

## Scaling and Load Balancing

### Horizontal Scaling

```bash
# Scale application instances
docker-compose up -d --scale app=5

# Using Docker Swarm
docker service scale orchestrator_app=5
```

### Load Balancer Configuration

**nginx.conf:**

```nginx
upstream app_servers {
    server app_1:8501 weight=1 max_fails=3 fail_timeout=30s;
    server app_2:8501 weight=1 max_fails=3 fail_timeout=30s;
    server app_3:8501 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
    }
}
```

### Auto-scaling with Docker Swarm

```yaml
version: '3.8'
services:
  app:
    image: freepik/ai-orchestrator:latest
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s
      placement:
        constraints:
          - node.role == worker
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G
```

## Monitoring and Logging

### Health Checks

Add health checks to your containers:

```yaml
services:
  app:
    image: freepik/ai-orchestrator:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Logging Configuration

**docker-compose.yml:**

```yaml
services:
  app:
    image: freepik/ai-orchestrator:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=ai-orchestrator"
```

### Centralized Logging

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  elasticsearch-data:
```

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs app

# Check container status
docker ps -a

# Inspect container
docker inspect ai-orchestrator

# Check resource usage
docker stats
```

#### Database Connection Issues

```bash
# Test database connectivity
docker-compose exec app ping postgres

# Check database logs
docker-compose logs postgres

# Connect to database manually
docker-compose exec postgres psql -U postgres -d orchestrator
```

#### Permission Issues

```bash
# Fix ownership
sudo chown -R $(id -u):$(id -g) ./data ./logs

# Set correct permissions
chmod 755 ./data ./logs
```

#### Out of Memory

```bash
# Check memory usage
docker stats

# Increase memory limit
docker-compose down
# Edit docker-compose.yml to add memory limits
docker-compose up -d
```

### Debugging Commands

```bash
# Enter container shell
docker-compose exec app bash

# Run commands inside container
docker-compose exec app python manage.py shell

# Copy files from container
docker cp ai-orchestrator:/app/logs/app.log ./local-logs/

# View real-time logs
docker-compose logs -f --tail=100 app

# Check container processes
docker-compose exec app ps aux

# Network diagnostics
docker network ls
docker network inspect orchestrator_default
```

### Performance Tuning

#### Resource Limits

```yaml
services:
  app:
    image: freepik/ai-orchestrator:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

#### Database Optimization

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: orchestrator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    command: >
      postgres
      -c shared_preload_libraries=pg_stat_statements
      -c max_connections=200
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
```

#### Redis Optimization

```yaml
services:
  redis:
    image: redis:7-alpine
    command: >
      redis-server
      --maxmemory 1gb
      --maxmemory-policy allkeys-lru
      --appendonly yes
      --appendfsync everysec
```

For more deployment options and advanced configurations, see the [Production Deployment Guide](production.md).
