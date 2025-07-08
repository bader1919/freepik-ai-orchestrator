# Production Deployment Best Practices

This guide covers best practices and considerations for deploying the Freepik AI Orchestrator in production environments.

## Table of Contents

- [Production Readiness Checklist](#production-readiness-checklist)
- [Infrastructure Requirements](#infrastructure-requirements)
- [Security Hardening](#security-hardening)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Observability](#monitoring-and-observability)
- [High Availability Setup](#high-availability-setup)
- [Disaster Recovery](#disaster-recovery)
- [CI/CD Pipeline](#cicd-pipeline)
- [Maintenance and Updates](#maintenance-and-updates)
- [Cost Optimization](#cost-optimization)

## Production Readiness Checklist

### Pre-Deployment

- [ ] **Security audit completed**
- [ ] **Load testing performed**
- [ ] **Backup strategy implemented**
- [ ] **Monitoring setup configured**
- [ ] **SSL certificates obtained**
- [ ] **Environment variables secured**
- [ ] **Database migrations tested**
- [ ] **API rate limiting configured**
- [ ] **Error tracking enabled**
- [ ] **Log aggregation setup**

### Infrastructure

- [ ] **Auto-scaling configured**
- [ ] **Health checks implemented**
- [ ] **Resource limits set**
- [ ] **Network security groups configured**
- [ ] **CDN setup for static assets**
- [ ] **Database connection pooling**
- [ ] **Redis clustering (if needed)**
- [ ] **File storage configured**

### Operations

- [ ] **Deployment automation**
- [ ] **Rollback procedures documented**
- [ ] **Incident response plan**
- [ ] **Performance benchmarks established**
- [ ] **Documentation updated**
- [ ] **Team training completed**

## Infrastructure Requirements

### Minimum Production Requirements

| Component | Specification | Recommendation |
|-----------|---------------|----------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8GB | 16GB+ |
| Storage | 100GB SSD | 500GB+ SSD |
| Network | 1Gbps | 10Gbps |
| Database | PostgreSQL 12+ | PostgreSQL 15+ |
| Cache | Redis 6+ | Redis 7+ |

### Recommended Architecture

```
Internet
    |
[Load Balancer]
    |
[Web Application Firewall]
    |
[Application Servers] (3+ instances)
    |
[Database Cluster] (Primary + Replicas)
    |
[Cache Cluster] (Redis)
    |
[File Storage] (S3/MinIO)
```

### Cloud Provider Configurations

#### AWS

```yaml
# EC2 Instance Recommendations
Instance Type: c5.2xlarge or m5.2xlarge
OS: Amazon Linux 2 or Ubuntu 20.04 LTS
EBS: gp3 with 3000 IOPS
VPC: Private subnets with NAT Gateway
Security Groups: Restrictive inbound rules

# RDS Configuration
Engine: PostgreSQL 15
Instance: db.r5.xlarge
Storage: gp3 with 3000 IOPS
Multi-AZ: Enabled
Backup: 7-day retention

# ElastiCache
Engine: Redis 7
Node: cache.r6g.large
Cluster Mode: Enabled
Backup: Enabled
```

#### Azure

```yaml
# Virtual Machine
Size: Standard_D4s_v3
OS: Ubuntu 20.04 LTS
Disk: Premium SSD P30
Network: Virtual Network with NSG
Availability: Availability Set

# Azure Database for PostgreSQL
Tier: General Purpose
vCores: 4
Storage: 500GB
Backup: 7-day retention
High Availability: Enabled

# Azure Cache for Redis
Tier: Premium P1
Clustering: Enabled
Persistence: Enabled
```

#### Google Cloud Platform

```yaml
# Compute Engine
Machine Type: n2-standard-4
OS: Ubuntu 20.04 LTS
Disk: SSD Persistent Disk 500GB
Network: VPC with Firewall Rules
Availability: Multi-zone

# Cloud SQL
Version: PostgreSQL 15
Tier: db-custom-4-16384
Storage: 500GB SSD
High Availability: Regional
Backup: Automated daily

# Memorystore for Redis
Tier: Standard
Memory: 5GB
High Availability: Enabled
```

## Security Hardening

### Network Security

#### Firewall Configuration

```bash
# Allow HTTP/HTTPS only
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow SSH from specific IPs only
iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 22 -j ACCEPT

# Block all other incoming traffic
iptables -P INPUT DROP
iptables -P FORWARD DROP
```

#### SSL/TLS Configuration

**nginx.conf:**

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'";
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Application Security

#### Environment Variables Management

Use a secrets management system:

```bash
# Using AWS Secrets Manager
aws secretsmanager create-secret \
    --name freepik-ai-orchestrator/prod \
    --secret-string '{
        "OPENAI_API_KEY": "sk-your-key",
        "DATABASE_URL": "postgresql://...",
        "SECRET_KEY": "your-secret-key"
    }'

# Retrieve in application
SECRET=$(aws secretsmanager get-secret-value \
    --secret-id freepik-ai-orchestrator/prod \
    --query SecretString --output text)
```

#### API Security

```python
# Rate limiting implementation
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/v1/generate")
@limiter.limit("10 per minute")
def generate():
    # API implementation
    pass

# Input validation
from marshmallow import Schema, fields, validate

class GenerationSchema(Schema):
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    model = fields.Str(required=True, validate=validate.OneOf(['dall-e-3', 'midjourney']))
    size = fields.Str(validate=validate.OneOf(['512x512', '1024x1024']))
```

#### Database Security

```sql
-- Create limited user for application
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE orchestrator TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Enable row-level security
ALTER TABLE generations ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_generations ON generations FOR ALL TO app_user USING (user_id = current_user_id());
```

## Performance Optimization

### Application Level

#### Caching Strategy

```python
# Redis caching implementation
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='redis', port=6379, db=0)

def cache_result(expiration=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiration=1800)
def generate_content(prompt, model):
    # Expensive generation operation
    return result
```

#### Database Optimization

```sql
-- Create indexes for frequently queried columns
CREATE INDEX CONCURRENTLY idx_generations_user_id ON generations(user_id);
CREATE INDEX CONCURRENTLY idx_generations_created_at ON generations(created_at);
CREATE INDEX CONCURRENTLY idx_generations_model ON generations(model);

-- Optimize queries with proper indexing
CREATE INDEX CONCURRENTLY idx_generations_composite 
    ON generations(user_id, created_at DESC, model);

-- Partition large tables
CREATE TABLE generations_2024_01 PARTITION OF generations 
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

#### Connection Pooling

```python
# PostgreSQL connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### Infrastructure Level

#### Load Balancing

```yaml
# HAProxy configuration
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend ai_orchestrator_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/your-domain.pem
    redirect scheme https if !{ ssl_fc }
    default_backend ai_orchestrator_backend

backend ai_orchestrator_backend
    balance roundrobin
    option httpchk GET /health
    server app1 10.0.1.10:8501 check
    server app2 10.0.1.11:8501 check
    server app3 10.0.1.12:8501 check
```

#### Auto-scaling Configuration

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-orchestrator-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-orchestrator
  minReplicas: 3
  maxReplicas: 20
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

## Monitoring and Observability

### Application Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
GENERATION_REQUESTS = Counter('generation_requests_total', 'Total generation requests', ['model', 'status'])
GENERATION_DURATION = Histogram('generation_duration_seconds', 'Generation duration', ['model'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

# Use in application
@app.route('/api/v1/generate')
def generate():
    start_time = time.time()
    try:
        result = perform_generation(prompt, model)
        GENERATION_REQUESTS.labels(model=model, status='success').inc()
        return result
    except Exception as e:
        GENERATION_REQUESTS.labels(model=model, status='error').inc()
        raise
    finally:
        GENERATION_DURATION.labels(model=model).observe(time.time() - start_time)
```

### Monitoring Stack

#### Prometheus Configuration

**prometheus.yml:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'ai-orchestrator'
    static_configs:
      - targets: ['app:8000']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

#### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "AI Orchestrator Metrics",
    "panels": [
      {
        "title": "Generation Requests per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(generation_requests_total[5m])",
            "legendFormat": "{{model}} - {{status}}"
          }
        ]
      },
      {
        "title": "Average Generation Time",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(generation_duration_seconds_sum[5m]) / rate(generation_duration_seconds_count[5m])",
            "legendFormat": "{{model}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

**alert_rules.yml:**

```yaml
groups:
  - name: ai-orchestrator
    rules:
      - alert: HighErrorRate
        expr: rate(generation_requests_total{status="error"}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighResponseTime
        expr: rate(generation_duration_seconds_sum[5m]) / rate(generation_duration_seconds_count[5m]) > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "Average response time is {{ $value }} seconds"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"
```

## High Availability Setup

### Database High Availability

#### PostgreSQL Streaming Replication

**Primary Server:**

```bash
# postgresql.conf
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
synchronous_commit = on
synchronous_standby_names = 'standby1'

# pg_hba.conf
host replication replicator 10.0.1.0/24 md5
```

**Standby Server:**

```bash
# recovery.conf (PostgreSQL < 12) or postgresql.conf (PostgreSQL 12+)
primary_conninfo = 'host=10.0.1.10 port=5432 user=replicator password=password'
hot_standby = on
```

#### Automatic Failover with Patroni

**patroni.yml:**

```yaml
scope: postgres-cluster
namespace: /service/
name: postgres-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.1.10:8008

etcd:
  hosts: 10.0.1.20:2379,10.0.1.21:2379,10.0.1.22:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 30
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        wal_level: replica
        hot_standby: "on"
        max_connections: 200
        max_worker_processes: 8
        max_wal_senders: 8
        max_replication_slots: 8

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.1.10:5432
  data_dir: /var/lib/postgresql/data
  bin_dir: /usr/lib/postgresql/15/bin
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: replicator_password
    superuser:
      username: postgres
      password: postgres_password
```

### Redis High Availability

#### Redis Sentinel Configuration

**sentinel.conf:**

```bash
port 26379
sentinel monitor redis-cluster 10.0.1.30 6379 2
sentinel down-after-milliseconds redis-cluster 5000
sentinel failover-timeout redis-cluster 60000
sentinel parallel-syncs redis-cluster 1
```

#### Application Configuration for Redis Cluster

```python
import redis.sentinel

# Redis Sentinel configuration
sentinels = [
    ('10.0.1.40', 26379),
    ('10.0.1.41', 26379),
    ('10.0.1.42', 26379)
]

sentinel = redis.sentinel.Sentinel(sentinels, socket_timeout=0.1)

# Get master and slave connections
redis_master = sentinel.master_for('redis-cluster', socket_timeout=0.1)
redis_slave = sentinel.slave_for('redis-cluster', socket_timeout=0.1)
```

## Disaster Recovery

### Backup Strategy

#### Database Backups

```bash
#!/bin/bash
# backup.sh - Database backup script

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="orchestrator"

# Create backup
pg_dump -h localhost -U postgres -d $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://your-backup-bucket/database/

# Cleanup old local backups (keep 7 days)
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

# Verify backup integrity
gunzip -t $BACKUP_DIR/db_backup_$DATE.sql.gz
if [ $? -eq 0 ]; then
    echo "Backup successful: db_backup_$DATE.sql.gz"
else
    echo "Backup verification failed!" >&2
    exit 1
fi
```

#### Application State Backup

```bash
#!/bin/bash
# app_backup.sh - Application state backup

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup configuration files
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz /app/config/

# Backup user uploads
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz /app/uploads/

# Backup logs
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /app/logs/

# Upload to S3
aws s3 sync $BACKUP_DIR s3://your-backup-bucket/application/
```

### Recovery Procedures

#### Database Recovery

```bash
#!/bin/bash
# restore.sh - Database restore script

BACKUP_FILE=$1
DB_NAME="orchestrator"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop application
docker-compose stop app

# Drop and recreate database
psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -h localhost -U postgres -c "CREATE DATABASE $DB_NAME;"

# Restore from backup
gunzip -c $BACKUP_FILE | psql -h localhost -U postgres -d $DB_NAME

# Start application
docker-compose start app

echo "Database restored from $BACKUP_FILE"
```

### Testing Recovery Procedures

```bash
#!/bin/bash
# test_recovery.sh - Test recovery procedures

# Create test environment
docker-compose -f docker-compose.test.yml up -d

# Restore backup to test environment
./restore.sh /backups/db_backup_latest.sql.gz

# Run verification tests
python -m pytest tests/integration/test_recovery.py

# Cleanup test environment
docker-compose -f docker-compose.test.yml down -v
```

## CI/CD Pipeline

### GitHub Actions Workflow

**.github/workflows/deploy.yml:**

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run tests
        run: pytest --cov=freepik_ai_orchestrator
      
      - name: Security scan
        run: bandit -r freepik_ai_orchestrator/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          push: true
          tags: |
            freepik/ai-orchestrator:latest
            freepik/ai-orchestrator:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        run: |
          echo "${{ secrets.STAGING_SSH_KEY }}" > staging_key
          chmod 600 staging_key
          ssh -i staging_key -o StrictHostKeyChecking=no \
            deploy@staging.yourdomain.com \
            "cd /app && docker-compose pull && docker-compose up -d"
      
      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://staging.yourdomain.com/health
      
      - name: Deploy to production
        if: success()
        run: |
          echo "${{ secrets.PRODUCTION_SSH_KEY }}" > production_key
          chmod 600 production_key
          ssh -i production_key -o StrictHostKeyChecking=no \
            deploy@production.yourdomain.com \
            "cd /app && docker-compose pull && docker-compose up -d"
```

### Blue-Green Deployment

```bash
#!/bin/bash
# deploy.sh - Blue-green deployment script

NEW_VERSION=$1
CURRENT_ENV=$(cat /app/current_env)

if [ "$CURRENT_ENV" = "blue" ]; then
    NEW_ENV="green"
    OLD_ENV="blue"
else
    NEW_ENV="blue"
    OLD_ENV="green"
fi

echo "Deploying version $NEW_VERSION to $NEW_ENV environment"

# Update new environment
docker-compose -f docker-compose.$NEW_ENV.yml pull
docker-compose -f docker-compose.$NEW_ENV.yml up -d

# Wait for health check
sleep 30
if curl -f http://localhost:808${NEW_ENV}/health; then
    echo "New environment is healthy, switching traffic"
    
    # Update load balancer
    sed -i "s/808${OLD_ENV}/808${NEW_ENV}/g" /etc/nginx/nginx.conf
    nginx -s reload
    
    # Update current environment marker
    echo $NEW_ENV > /app/current_env
    
    # Stop old environment
    docker-compose -f docker-compose.$OLD_ENV.yml down
    
    echo "Deployment successful"
else
    echo "New environment failed health check, rolling back"
    docker-compose -f docker-compose.$NEW_ENV.yml down
    exit 1
fi
```

## Maintenance and Updates

### Rolling Updates

```bash
#!/bin/bash
# rolling_update.sh - Perform rolling update

NEW_IMAGE=$1
INSTANCES=("app1" "app2" "app3")

for instance in "${INSTANCES[@]}"; do
    echo "Updating $instance..."
    
    # Remove from load balancer
    curl -X POST "http://loadbalancer:8080/admin/disable/$instance"
    
    # Wait for connections to drain
    sleep 30
    
    # Update instance
    docker service update --image $NEW_IMAGE orchestrator_$instance
    
    # Wait for health check
    while ! curl -f "http://$instance:8501/health"; do
        echo "Waiting for $instance to be healthy..."
        sleep 10
    done
    
    # Add back to load balancer
    curl -X POST "http://loadbalancer:8080/admin/enable/$instance"
    
    echo "$instance updated successfully"
done
```

### Database Migrations

```python
# migrations/migrate.py
import sys
import psycopg2
from pathlib import Path

def run_migration(db_url, migration_file):
    """Run a single migration file."""
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    try:
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        cursor.execute(migration_sql)
        conn.commit()
        
        # Record migration
        cursor.execute(
            "INSERT INTO migrations (filename, applied_at) VALUES (%s, NOW())",
            (migration_file.name,)
        )
        conn.commit()
        
        print(f"Applied migration: {migration_file.name}")
        
    except Exception as e:
        conn.rollback()
        print(f"Failed to apply migration {migration_file.name}: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

def main():
    db_url = os.environ['DATABASE_URL']
    migrations_dir = Path('migrations')
    
    # Get applied migrations
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM migrations")
    applied = {row[0] for row in cursor.fetchall()}
    cursor.close()
    conn.close()
    
    # Apply pending migrations
    for migration_file in sorted(migrations_dir.glob('*.sql')):
        if migration_file.name not in applied:
            run_migration(db_url, migration_file)

if __name__ == '__main__':
    main()
```

## Cost Optimization

### Resource Optimization

#### Auto-scaling Configuration

```yaml
# Kubernetes VPA (Vertical Pod Autoscaler)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ai-orchestrator-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-orchestrator
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: ai-orchestrator
      maxAllowed:
        cpu: 2000m
        memory: 4Gi
      minAllowed:
        cpu: 100m
        memory: 256Mi
```

#### Spot Instance Usage

```yaml
# AWS Auto Scaling Group with Spot Instances
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MixedInstancesPolicy:
        InstancesDistribution:
          OnDemandPercentage: 20
          SpotAllocationStrategy: diversified
        LaunchTemplate:
          LaunchTemplateSpecification:
            LaunchTemplateId: !Ref LaunchTemplate
            Version: !GetAtt LaunchTemplate.LatestVersionNumber
          Overrides:
            - InstanceType: c5.large
            - InstanceType: c5.xlarge
            - InstanceType: m5.large
            - InstanceType: m5.xlarge
```

### Cost Monitoring

```python
# cost_monitor.py - Monitor and alert on costs
import boto3
import datetime
from decimal import Decimal

def get_monthly_cost():
    """Get current month's AWS costs."""
    client = boto3.client('ce')
    
    start = datetime.date.today().replace(day=1).strftime('%Y-%m-%d')
    end = datetime.date.today().strftime('%Y-%m-%d')
    
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    
    total_cost = Decimal('0')
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            amount = Decimal(group['Metrics']['BlendedCost']['Amount'])
            total_cost += amount
            service = group['Keys'][0]
            print(f"{service}: ${amount:.2f}")
    
    print(f"Total monthly cost: ${total_cost:.2f}")
    return total_cost

def cost_alert(threshold=1000):
    """Send alert if cost exceeds threshold."""
    cost = get_monthly_cost()
    if cost > threshold:
        # Send alert (email, Slack, etc.)
        send_alert(f"Monthly cost ${cost:.2f} exceeds threshold ${threshold}")

if __name__ == '__main__':
    cost_alert()
```

This comprehensive production deployment guide covers all aspects of running the Freepik AI Orchestrator in a production environment, ensuring security, reliability, performance, and cost-effectiveness.
