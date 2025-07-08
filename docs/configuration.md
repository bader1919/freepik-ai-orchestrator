# Configuration Guide

This guide covers all configuration options available in the Freepik AI Orchestrator.

## Environment Variables

The application uses environment variables for configuration. These can be set in a `.env` file or directly in your environment.

### Core Configuration

#### Freepik API Settings

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FREEPIK_API_KEY` | Your Freepik API key | Yes | - |
| `FREEPIK_BASE_URL` | Freepik API base URL | No | `https://api.freepik.com` |
| `FREEPIK_TIMEOUT` | API request timeout (seconds) | No | `30` |
| `FREEPIK_RETRY_COUNT` | Number of retry attempts | No | `3` |

#### LLM Provider Settings

Choose one of the following LLM providers:

##### OpenAI Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes* | - |
| `OPENAI_MODEL` | Model to use | No | `gpt-4` |
| `OPENAI_MAX_TOKENS` | Maximum tokens per request | No | `1000` |
| `OPENAI_TEMPERATURE` | Response creativity (0-1) | No | `0.7` |

##### Anthropic Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes* | - |
| `ANTHROPIC_MODEL` | Model to use | No | `claude-3-sonnet-20240229` |
| `ANTHROPIC_MAX_TOKENS` | Maximum tokens per request | No | `1000` |

*One LLM provider is required

### Application Settings

#### General Settings

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `APP_ENV` | Environment (development/production) | No | `development` |
| `DEBUG` | Enable debug mode | No | `false` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `SECRET_KEY` | Application secret key | No | Auto-generated |

#### Database Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | No | `sqlite:///freepik_orchestrator.db` |
| `DB_POOL_SIZE` | Connection pool size | No | `5` |
| `DB_MAX_OVERFLOW` | Maximum overflow connections | No | `10` |

#### Streamlit Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `STREAMLIT_SERVER_PORT` | Server port | No | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Server address | No | `0.0.0.0` |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Collect usage stats | No | `false` |
| `STREAMLIT_SERVER_ENABLE_CORS` | Enable CORS | No | `false` |

### Advanced Configuration

#### Webhook Settings

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WEBHOOK_URL` | Webhook endpoint URL | No | - |
| `WEBHOOK_SECRET` | Webhook secret for verification | No | - |
| `WEBHOOK_TIMEOUT` | Webhook timeout (seconds) | No | `30` |

#### Caching Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CACHE_TYPE` | Cache backend (memory/redis) | No | `memory` |
| `REDIS_URL` | Redis connection URL | No | - |
| `CACHE_DEFAULT_TIMEOUT` | Default cache timeout (seconds) | No | `300` |

#### Rate Limiting

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `RATE_LIMIT_ENABLED` | Enable rate limiting | No | `true` |
| `RATE_LIMIT_PER_MINUTE` | Requests per minute | No | `60` |
| `RATE_LIMIT_PER_HOUR` | Requests per hour | No | `1000` |

## Configuration Files

### Streamlit Configuration

Create a `.streamlit/config.toml` file for Streamlit-specific settings:

```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Logging Configuration

Create a `logging.yaml` file for detailed logging configuration:

```yaml
version: 1
disable_existing_loggers: false

formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: default
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

root:
  level: INFO
  handlers: [console, file]

loggers:
  freepik_orchestrator:
    level: DEBUG
    handlers: [console, file]
    propagate: false
  
  streamlit:
    level: WARNING
    handlers: [console]
    propagate: false
```

## Model Configuration

### Image Generation Models

Configure available models in your application:

```python
# config/models.py
AVAILABLE_MODELS = {
    "mystic": {
        "name": "Mystic",
        "description": "High-quality artistic images",
        "max_resolution": "1024x1024",
        "pricing_tier": "premium"
    },
    "imagen3": {
        "name": "Imagen 3",
        "description": "Google's latest image model",
        "max_resolution": "1536x1536",
        "pricing_tier": "premium"
    },
    "flux_dev": {
        "name": "Flux Dev",
        "description": "Fast development model",
        "max_resolution": "1024x1024",
        "pricing_tier": "standard"
    },
    "classic_fast": {
        "name": "Classic Fast",
        "description": "Quick generation model",
        "max_resolution": "512x512",
        "pricing_tier": "basic"
    }
}
```

### Post-Processing Configuration

```python
# config/post_processing.py
POST_PROCESSING_OPTIONS = {
    "upscaling": {
        "enabled": True,
        "max_scale": 4,
        "algorithms": ["esrgan", "real_esrgan", "waifu2x"]
    },
    "background_removal": {
        "enabled": True,
        "models": ["u2net", "silueta"]
    },
    "style_transfer": {
        "enabled": True,
        "styles": ["artistic", "photographic", "cartoon"]
    },
    "relighting": {
        "enabled": True,
        "presets": ["natural", "dramatic", "soft"]
    }
}
```

## Security Configuration

### API Key Management

For production deployments, consider using a secrets management system:

```bash
# Using AWS Secrets Manager
export FREEPIK_API_KEY=$(aws secretsmanager get-secret-value --secret-id freepik-api-key --query SecretString --output text)

# Using Azure Key Vault
export FREEPIK_API_KEY=$(az keyvault secret show --vault-name your-vault --name freepik-api-key --query value -o tsv)

# Using HashiCorp Vault
export FREEPIK_API_KEY=$(vault kv get -field=api_key secret/freepik)
```

### HTTPS Configuration

For production, enable HTTPS:

```toml
# .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = true
sslCertFile = "/path/to/cert.pem"
sslKeyFile = "/path/to/key.pem"
```

## Performance Tuning

### Database Optimization

For PostgreSQL in production:

```bash
# Environment variables
DATABASE_URL=postgresql://user:password@localhost:5432/freepik_orchestrator
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### Caching Configuration

For Redis caching:

```bash
# Environment variables
CACHE_TYPE=redis
REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=3600
CACHE_KEY_PREFIX=freepik_orchestrator:
```

### Async Configuration

```bash
# Webhook and async processing
WEBHOOK_WORKERS=4
ASYNC_TIMEOUT=300
MAX_CONCURRENT_REQUESTS=10
```

## Monitoring Configuration

### Metrics and Analytics

```bash
# Monitoring settings
ENABLE_METRICS=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=true
GRAFANA_DASHBOARD_URL=http://localhost:3000
```

### Health Checks

```bash
# Health check configuration
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10
```

## Validation

Validate your configuration with the built-in validator:

```bash
python -c "from config.validator import validate_config; validate_config()"
```

This will check:
- Required environment variables
- API key validity
- Database connectivity
- LLM provider accessibility

## Configuration Examples

### Development Environment

```bash
# .env for development
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
FREEPIK_API_KEY=your_dev_key
OPENAI_API_KEY=your_openai_key
DATABASE_URL=sqlite:///dev.db
STREAMLIT_SERVER_PORT=8501
```

### Production Environment

```bash
# .env for production
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
FREEPIK_API_KEY=your_prod_key
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:pass@db:5432/freepik_orchestrator
CACHE_TYPE=redis
REDIS_URL=redis://redis:6379/0
RATE_LIMIT_ENABLED=true
WEBHOOK_URL=https://your-domain.com/webhook
```

## Next Steps

With your configuration complete:

1. **Test Configuration**: Run the configuration validator
2. **Start Application**: Launch the application with your settings
3. **Monitor**: Set up monitoring and logging
4. **Optimize**: Tune performance based on usage patterns

For detailed usage instructions, see the [Usage Guide](USAGE.md).
