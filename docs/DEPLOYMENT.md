# Deployment Guide

This guide covers deployment options for the Freepik AI Orchestrator in various environments.

## Prerequisites

- Docker and Docker Compose
- Domain name with SSL certificate
- API keys for Freepik and LLM providers
- PostgreSQL database (for production)

## Environment Setup

### 1. Environment Variables

Create a `.env` file with your configuration:

```bash
# Required
FREEPIK_API_KEY=your_freepik_api_key
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your-super-secret-key-here

# Production
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/dbname
FREEPIK_WEBHOOK_URL=https://yourdomain.com/webhook

# Optional
REDIS_URL=redis://localhost:6379/0
STRIPE_SECRET_KEY=sk_live_...
```

### 2. SSL Certificate

Ensure you have SSL certificates for HTTPS:

```bash
# Using Certbot (Let's Encrypt)
sudo certbot certonly --standalone -d yourdomain.com
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

**1. Clone and Configure**
```bash
git clone https://github.com/yourusername/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator
cp .env.example .env
# Edit .env with your values
```

**2. Deploy with Docker Compose**
```bash
docker-compose up -d
```

**3. Verify Deployment**
```bash
docker-compose ps
curl https://yourdomain.com:8501/health
```

### Option 2: Kubernetes

**1. Create Namespace**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: freepik-orchestrator
```

**2. Create ConfigMap**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: freepik-orchestrator
data:
  ENVIRONMENT: "production"
  DATABASE_URL: "postgresql://user:pass@postgres:5432/freepik_orchestrator"
```

**3. Create Secret**
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
```

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
