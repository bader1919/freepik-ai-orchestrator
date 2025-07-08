# Deployment Guide

Complete deployment guide for the Freepik AI Orchestrator across different environments and platforms.

## Overview

This guide covers deployment strategies from local development to production-grade deployments on cloud platforms. Choose the deployment method that best fits your infrastructure and requirements.

## Prerequisites

Before deploying, ensure you have:

- **Docker & Docker Compose**: For containerized deployments
- **Domain & SSL Certificate**: For production HTTPS access
- **API Keys**: Freepik API key and LLM provider credentials
- **Database**: PostgreSQL for production (SQLite for development)
- **Cloud Account**: AWS, GCP, or Azure for cloud deployments

## Quick Deployment

### Local Development

For local development and testing:

```bash
# Clone repository
git clone https://github.com/yourusername/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up --build
```

Access the application at `http://localhost:8501`

### Production Quick Start

For production deployment:

```bash
# Clone and configure
git clone https://github.com/yourusername/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator
cp .env.example .env.production

# Configure production environment
vim .env.production

# Deploy with production compose
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Configuration

### Development Environment

Create `.env` file for development:

```bash
# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG

# API Keys
FREEPIK_API_KEY=your_freepik_dev_key
OPENAI_API_KEY=your_openai_dev_key

# Database
DATABASE_URL=sqlite:///dev.db

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Production Environment

Create `.env.production` file:

```bash
# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=your-super-secret-production-key

# API Keys
FREEPIK_API_KEY=your_freepik_production_key
OPENAI_API_KEY=your_openai_production_key

# Database
DATABASE_URL=postgresql://user:password@db.example.com:5432/freepik_orchestrator
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# Redis Cache
REDIS_URL=redis://redis.example.com:6379/0
CACHE_DEFAULT_TIMEOUT=3600

# Webhook
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_SECRET=your_webhook_secret

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
PROMETHEUS_ENABLED=true

# Security
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
ENABLE_CORS=false
```

## Docker Deployment

### Development Docker Compose

The default `docker-compose.yml` for development:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - APP_ENV=development
    env_file:
      - .env
    volumes:
      - .:/app
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: freepik_orchestrator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Production Docker Compose

Create `docker-compose.prod.yml` for production:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - APP_ENV=production
    env_file:
      - .env.production
    depends_on:
      - db
      - redis
    networks:
      - app-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.freepik-orchestrator.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.freepik-orchestrator.tls.certresolver=letsencrypt"

  db:
    image: postgres:14
    restart: unless-stopped
    environment:
      POSTGRES_DB: freepik_orchestrator
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/migrations:/docker-entrypoint-initdb.d
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - app-network

  traefik:
    image: traefik:v3.0
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik.yml:/etc/traefik/traefik.yml
      - traefik_certs:/certs
    networks:
      - app-network

  prometheus:
    image: prom/prometheus
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - app-network

  grafana:
    image: grafana/grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:
  traefik_certs:
  prometheus_data:
  grafana_data:

networks:
  app-network:
    driver: bridge
```

### Production Dockerfile

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/health || exit 1

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Cloud Platform Deployments

### AWS Deployment

#### AWS ECS with Fargate

1. **Create ECS Cluster**

```bash
aws ecs create-cluster --cluster-name freepik-orchestrator
```

2. **Create Task Definition**

```json
{
  "family": "freepik-orchestrator",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "your-registry/freepik-orchestrator:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "APP_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "FREEPIK_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:freepik-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/freepik-orchestrator",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

3. **Create Service**

```bash
aws ecs create-service \
  --cluster freepik-orchestrator \
  --service-name freepik-orchestrator-service \
  --task-definition freepik-orchestrator \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

#### AWS Lambda + API Gateway

For serverless deployment:

```python
# lambda_handler.py
import json
from core.llm_orchestrator import LLMOrchestrator
from core.freepik_client import FreepikClient

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        prompt = body.get('prompt')
        
        orchestrator = LLMOrchestrator()
        client = FreepikClient()
        
        enhanced_prompt = orchestrator.enhance_prompt(prompt)
        result = client.generate_image(enhanced_prompt)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Google Cloud Platform

#### Cloud Run Deployment

1. **Build and Push Container**

```bash
# Build image
docker build -t gcr.io/your-project/freepik-orchestrator .

# Push to Container Registry
docker push gcr.io/your-project/freepik-orchestrator
```

2. **Deploy to Cloud Run**

```bash
gcloud run deploy freepik-orchestrator \
  --image gcr.io/your-project/freepik-orchestrator \
  --platform managed \
  --region us-central1 \
  --set-env-vars APP_ENV=production \
  --set-secrets FREEPIK_API_KEY=freepik-api-key:latest \
  --allow-unauthenticated
```

3. **Cloud Run YAML Configuration**

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: freepik-orchestrator
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project/freepik-orchestrator
        ports:
        - containerPort: 8501
        env:
        - name: APP_ENV
          value: production
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
```

### Microsoft Azure

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name freepik-orchestrator \
  --image your-registry/freepik-orchestrator:latest \
  --ports 8501 \
  --dns-name-label freepik-orchestrator \
  --environment-variables APP_ENV=production \
  --secure-environment-variables FREEPIK_API_KEY=your-key
```

#### Azure App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name freepik-orchestrator-plan \
  --resource-group myResourceGroup \
  --sku P1V2 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group myResourceGroup \
  --plan freepik-orchestrator-plan \
  --name freepik-orchestrator \
  --deployment-container-image-name your-registry/freepik-orchestrator:latest
```

## Kubernetes Deployment

### Complete Kubernetes Manifests

#### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: freepik-orchestrator
  labels:
    name: freepik-orchestrator
```

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: freepik-orchestrator
data:
  APP_ENV: "production"
  LOG_LEVEL: "INFO"
  STREAMLIT_SERVER_PORT: "8501"
  REDIS_URL: "redis://redis-service:6379/0"
```

#### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: freepik-orchestrator
type: Opaque
stringData:
  FREEPIK_API_KEY: "your_freepik_api_key"
  OPENAI_API_KEY: "your_openai_key"
  SECRET_KEY: "your-super-secret-key"
  DATABASE_URL: "postgresql://user:pass@postgres-service:5432/freepik_orchestrator"
```

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: freepik-orchestrator
  namespace: freepik-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: freepik-orchestrator
  template:
    metadata:
      labels:
        app: freepik-orchestrator
    spec:
      containers:
      - name: app
        image: your-registry/freepik-orchestrator:latest
        ports:
        - containerPort: 8501
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8501
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: freepik-orchestrator-service
  namespace: freepik-orchestrator
spec:
  selector:
    app: freepik-orchestrator
  ports:
  - port: 80
    targetPort: 8501
  type: ClusterIP
```

#### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: freepik-orchestrator-ingress
  namespace: freepik-orchestrator
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: freepik-orchestrator-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: freepik-orchestrator-service
            port:
              number: 80
```

## Monitoring and Observability

### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'freepik-orchestrator'
    static_configs:
      - targets: ['app:8501']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Freepik AI Orchestrator",
    "panels": [
      {
        "title": "Image Generations",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(freepik_generations_total[5m])",
            "legendFormat": "Generations per second"
          }
        ]
      },
      {
        "title": "Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(freepik_generations_success_total[5m]) / rate(freepik_generations_total[5m]) * 100",
            "legendFormat": "Success Rate %"
          }
        ]
      }
    ]
  }
}
```

## Security Considerations

### Network Security

1. **Use HTTPS Only**
   - Configure SSL/TLS certificates
   - Redirect HTTP to HTTPS
   - Use HSTS headers

2. **Network Isolation**
   - Use private networks for database
   - Implement security groups/firewall rules
   - Restrict access to management ports

3. **API Security**
   - Rate limiting
   - API key rotation
   - Input validation

### Application Security

```python
# Security middleware example
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=APIKeyAuthenticationBackend()
)
```

### Secret Management

#### AWS Secrets Manager

```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Usage
freepik_api_key = get_secret('freepik-api-key')
```

#### Kubernetes Secrets

```bash
# Create secret from command line
kubectl create secret generic app-secrets \
  --from-literal=freepik-api-key=your-key \
  --from-literal=openai-api-key=your-key \
  -n freepik-orchestrator
```

## Scaling and Performance

### Horizontal Scaling

#### Auto-scaling Configuration

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: freepik-orchestrator-hpa
  namespace: freepik-orchestrator
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: freepik-orchestrator
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Database Scaling

#### PostgreSQL High Availability

```yaml
# Using PostgreSQL operator
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster
  namespace: freepik-orchestrator
spec:
  instances: 3
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
      effective_cache_size: "1GB"
  
  storage:
    size: 100Gi
    storageClass: fast-ssd
  
  backup:
    schedule: "0 2 * * *"
    target: s3
```

### Caching Strategy

#### Redis Cluster

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
  namespace: freepik-orchestrator
spec:
  serviceName: redis-cluster
  replicas: 6
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        command:
        - redis-server
        - /etc/redis/redis.conf
        volumeMounts:
        - name: redis-config
          mountPath: /etc/redis
        - name: redis-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## Backup and Disaster Recovery

### Database Backup

```bash
#!/bin/bash
# backup.sh

# Database backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Upload to S3
aws s3 cp backup_*.sql s3://your-backup-bucket/database/

# Cleanup old local backups
find . -name "backup_*.sql" -mtime +7 -delete
```

### Application Backup

```yaml
# CronJob for automated backups
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: freepik-orchestrator
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14
            command:
            - /bin/bash
            - -c
            - |
              pg_dump $DATABASE_URL | gzip > /backup/backup_$(date +%Y%m%d_%H%M%S).sql.gz
              aws s3 cp /backup/ s3://your-backup-bucket/ --recursive
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: DATABASE_URL
          restartPolicy: OnFailure
```

## Maintenance and Updates

### Rolling Updates

```bash
# Update image version
kubectl set image deployment/freepik-orchestrator \
  app=your-registry/freepik-orchestrator:v1.2.0 \
  -n freepik-orchestrator

# Monitor rollout
kubectl rollout status deployment/freepik-orchestrator -n freepik-orchestrator

# Rollback if needed
kubectl rollout undo deployment/freepik-orchestrator -n freepik-orchestrator
```

### Database Migrations

```python
# migrations/migrate.py
from alembic import command
from alembic.config import Config

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
```

## Troubleshooting

### Common Issues

#### Application Won't Start

1. **Check environment variables**
```bash
kubectl logs deployment/freepik-orchestrator -n freepik-orchestrator
```

2. **Verify secrets**
```bash
kubectl get secrets -n freepik-orchestrator
kubectl describe secret app-secrets -n freepik-orchestrator
```

3. **Check resource limits**
```bash
kubectl describe pod -l app=freepik-orchestrator -n freepik-orchestrator
```

#### Performance Issues

1. **Check resource usage**
```bash
kubectl top pods -n freepik-orchestrator
```

2. **Review application metrics**
```bash
curl http://your-domain.com/metrics
```

3. **Database performance**
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Health Checks

```python
# health.py
from fastapi import APIRouter
from database.db import get_db_connection
import redis

router = APIRouter()

@router.get("/health")
async def health_check():
    checks = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
    
    # Database check
    try:
        db = get_db_connection()
        db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"
    
    # Redis check
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
    
    return checks
```

## Support and Documentation

For deployment support:

- **Documentation**: [docs.freepik-orchestrator.com](https://docs.freepik-orchestrator.com)
- **GitHub Issues**: [github.com/freepik-ai-orchestrator/issues](https://github.com/yourusername/freepik-ai-orchestrator/issues)
- **Discord Community**: [discord.gg/freepik-ai](https://discord.gg/freepik-ai)
- **Enterprise Support**: support@freepik-orchestrator.com

Ready to deploy? Start with the [Quick Deployment](#quick-deployment) section for your environment!

**4. Deploy Application**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: freepik-orchestrator
  namespace: freepik-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: freepik-orchestrator
  template:
    metadata:
      labels:
        app: freepik-orchestrator
    spec:
      containers:
      - name: app
        image: freepik-orchestrator:latest
        ports:
        - containerPort: 8501
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Option 3: Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set FREEPIK_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
docker build -t freepik-orchestrator .
docker tag freepik-orchestrator:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/freepik-orchestrator:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/freepik-orchestrator:latest

# Create ECS service
aws ecs create-service --cluster your-cluster --service-name freepik-orchestrator --task-definition freepik-orchestrator:1 --desired-count 2
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/freepik-orchestrator
gcloud run deploy --image gcr.io/PROJECT-ID/freepik-orchestrator --platform managed
```

## Database Setup

### PostgreSQL Production Setup

**1. Create Database**
```sql
CREATE DATABASE freepik_orchestrator;
CREATE USER freepik_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE freepik_orchestrator TO freepik_user;
```

**2. Run Migrations**
```bash
# Via Docker
docker-compose exec app python -c "
from database.db import db_manager
import asyncio
asyncio.run(db_manager.initialize())
"
```

### Redis Setup (Optional)

For caching and session management:

```bash
# Docker
docker run -d --name redis -p 6379:6379 redis:alpine

# Or add to docker-compose.yml (already included)
```

## SSL and Security

### 1. Reverse Proxy with Nginx

Create `nginx.conf`:
```nginx
upstream app {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/yourdomain.com.pem;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /webhook {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## Monitoring and Logging

### 1. Health Checks

The application includes health check endpoints:
- `GET /health` - Basic health check
- `GET /metrics` - Prometheus metrics

### 2. Logging Configuration

Configure centralized logging:

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. Monitoring with Prometheus

Add monitoring stack:

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
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
```

## Scaling Considerations

### Horizontal Scaling

1. **Stateless Design**: Ensure your application is stateless
2. **Database Connection Pooling**: Use connection pooling for PostgreSQL
3. **Load Balancing**: Use a load balancer for multiple instances

### Vertical Scaling

Adjust resource limits based on usage:

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## Backup and Recovery

### Database Backups

```bash
# Automated daily backups
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
PGPASSWORD=password pg_dump -h localhost -U freepik_user freepik_orchestrator > $BACKUP_DIR/backup_$DATE.sql

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### Application Data

```bash
# Backup user-generated content
rsync -av /app/uploads/ /backups/uploads/
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
sudo lsof -i :8501
sudo kill -9 PID
```

2. **Database Connection Failed**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql
# Check connection
psql -h localhost -U freepik_user -d freepik_orchestrator
```

3. **SSL Certificate Issues**
```bash
# Check certificate validity
openssl x509 -in /etc/ssl/certs/yourdomain.com.pem -text -noout
```

4. **Memory Issues**
```bash
# Check memory usage
free -h
docker stats
```

### Log Analysis

```bash
# Application logs
docker-compose logs -f app

# Database logs
docker-compose logs -f postgres

# Specific error patterns
docker-compose logs app | grep ERROR
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_tasks_user_status ON freepik_tasks(user_id, status);
CREATE INDEX idx_tasks_created_at ON freepik_tasks(created_at);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM freepik_tasks WHERE user_id = 'user123';
```

### 2. Application Optimization

- Enable Redis caching for frequent queries
- Use connection pooling for database connections
- Implement request rate limiting
- Optimize image processing pipelines

### 3. Infrastructure Optimization

- Use CDN for static assets
- Implement horizontal pod autoscaling (Kubernetes)
- Use read replicas for database queries
- Enable gzip compression

## Security Checklist

- [ ] SSL/TLS certificates configured
- [ ] API keys stored securely (not in code)
- [ ] Database credentials rotated regularly
- [ ] Firewall rules configured
- [ ] Regular security updates applied
- [ ] Webhook signature verification enabled
- [ ] Rate limiting implemented
- [ ] Input validation in place
- [ ] Logging and monitoring configured
- [ ] Backup and recovery tested
