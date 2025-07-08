# API Reference

Complete API documentation for the Freepik AI Orchestrator platform.

## Overview

The Freepik AI Orchestrator API provides programmatic access to our AI-powered image generation platform. The API supports synchronous and asynchronous image generation, workflow execution, and comprehensive management features.

### Key Features

- **REST API**: Standard HTTP methods and JSON responses
- **Authentication**: Secure API key-based authentication
- **Rate Limiting**: Built-in rate limiting with clear headers
- **Webhooks**: Real-time notifications for async operations
- **Error Handling**: Detailed error messages and codes
- **Pagination**: Efficient handling of large datasets

## Getting Started

### Base URL

All API requests should be made to:

```
https://api.freepik-orchestrator.com/v1
```

### Authentication

Include your API key in the Authorization header:

```bash
Authorization: Bearer YOUR_API_KEY
```

### Rate Limits

API requests are rate limited by plan:

| Plan | Requests/Minute | Requests/Hour |
|------|----------------|---------------|
| Free | 10 | 100 |
| Professional | 60 | 1,000 |
| Enterprise | 300 | 10,000 |

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## Core Endpoints

### Image Generation

#### Generate Image

Create a new image using AI models with LLM optimization.

**Endpoint:** `POST /generate`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Image description |
| `model` | string | No | AI model (auto, mystic, imagen3, flux_dev, classic_fast) |
| `style` | string | No | Style preset (photorealistic, artistic, cartoon) |
| `aspect_ratio` | string | No | Image dimensions (1:1, 16:9, 9:16, 4:3, 3:4) |
| `quality_level` | integer | No | Quality setting (1-10, default: 8) |
| `webhook_url` | string | No | Webhook URL for async notifications |
| `enhance_prompt` | boolean | No | Enable LLM prompt optimization (default: true) |

**Request Example:**

```bash
curl -X POST "https://api.freepik-orchestrator.com/v1/generate" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional headshot of a businesswoman in modern office",
    "model": "imagen3",
    "style": "photorealistic",
    "aspect_ratio": "1:1",
    "quality_level": 9,
    "webhook_url": "https://your-app.com/webhook"
  }'
```

**Response:**

```json
{
  "task_id": "task_12345",
  "model_used": "imagen3", 
  "status": "pending",
  "original_prompt": "Professional headshot of a businesswoman in modern office",
  "enhanced_prompt": "Professional business headshot of a confident businesswoman...",
  "estimated_completion_time": 45,
  "webhook_callback": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

For complete API documentation with all endpoints, error handling, and examples, please refer to the full API reference documentation.
      "status": "completed",
      "result_url": "https://cdn.freepik.com/step1.jpg"
    },
    {
      "step": 2,
      "action": "relight",
      "status": "running"
    }
  ]
}
```

#### List Available Workflows
Get a list of available workflow templates.

**Endpoint:** `GET /workflows`

**Response:**
```json
{
  "workflows": [
    {
      "id": "professional_headshot",
      "name": "Professional Headshot",
      "description": "High-quality professional headshots with optimal lighting",
      "estimated_time": "3-4 minutes",
      "estimated_cost": "$1.20",
      "steps_count": 4
    }
  ]
}
```

### Post-Processing

#### Upscale Image
Upscale an existing image.

**Endpoint:** `POST /post-process/upscale`

**Request Body:**
```json
{
  "image_url": "https://cdn.freepik.com/original.jpg",
  "scale_factor": 4,
  "webhook_url": "https://your-domain.com/webhook"
}
```

#### Relight Image
Apply professional lighting to an image.

**Endpoint:** `POST /post-process/relight`

**Request Body:**
```json
{
  "image_url": "https://cdn.freepik.com/original.jpg",
  "lighting_style": "professional",
  "webhook_url": "https://your-domain.com/webhook"
}
```

#### Remove Background
Remove background from an image.

**Endpoint:** `POST /post-process/remove-background`

**Request Body:**
```json
{
  "image_url": "https://cdn.freepik.com/original.jpg"
}
```

**Response (Synchronous):**
```json
{
  "result_url": "https://cdn.freepik.com/no-bg.png",
  "processing_time": 5
}
```

### Analytics

#### User Analytics
Get analytics for the authenticated user.

**Endpoint:** `GET /analytics/user?days=30`

**Response:**
```json
{
  "period_days": 30,
  "total_generations": 156,
  "successful_generations": 148,
  "failed_generations": 8,
  "success_rate": 94.9,
  "total_cost_cents": 4680,
  "average_processing_time": 42,
  "models_used": {
    "mystic": 70,
    "imagen3": 56,
    "flux-dev": 20,
    "classic-fast": 10
  },
  "daily_stats": [
    {
      "date": "2024-01-15",
      "generations": 12,
      "cost_cents": 360
    }
  ]
}
```

## Webhooks

Webhooks are used to notify your application when asynchronous operations complete.

### Webhook Payload

```json
{
  "event": "generation.completed",
  "task_id": "task_12345",
  "timestamp": "2024-01-15T10:30:45Z",
  "data": {
    "status": "completed",
    "image_url": "https://cdn.freepik.com/result.jpg",
    "thumbnail_url": "https://cdn.freepik.com/thumb.jpg",
    "model_used": "imagen3",
    "processing_time": 45
  }
}
```

### Webhook Security

Webhooks are signed using HMAC-SHA256. Verify the signature using the `X-Freepik-Signature` header:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_MODEL",
    "message": "The specified model 'invalid-model' is not supported",
    "details": {
      "supported_models": ["mystic", "imagen3", "flux-dev", "classic-fast"]
    }
  }
}
```

### Error Codes

- `INVALID_API_KEY` - API key is missing or invalid
- `INSUFFICIENT_CREDITS` - Account has insufficient credits
- `INVALID_MODEL` - Specified model is not supported
- `PROMPT_TOO_LONG` - Prompt exceeds maximum length
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `WEBHOOK_URL_INVALID` - Webhook URL is not accessible
- `TASK_NOT_FOUND` - Task ID does not exist
- `WORKFLOW_NOT_FOUND` - Workflow ID does not exist

## Rate Limits

- **Free Tier**: 10 requests per day
- **Professional**: 1000 requests per hour
- **Enterprise**: 10000 requests per hour

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit per time window
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Time when rate limit resets (Unix timestamp)

## SDKs

### Python SDK

```python
from freepik_orchestrator import FreepikClient

client = FreepikClient(api_key="your-api-key")

# Generate image
result = await client.generate(
    prompt="Professional headshot",
    model="auto"
)

# Execute workflow
workflow_result = await client.execute_workflow(
    "professional_headshot",
    prompt="Business portrait"
)
```

### JavaScript SDK

```javascript
import { FreepikClient } from '@freepik/orchestrator-js';

const client = new FreepikClient('your-api-key');

// Generate image
const result = await client.generate({
  prompt: 'Professional headshot',
  model: 'auto'
});

// Execute workflow
const workflowResult = await client.executeWorkflow(
  'professional_headshot',
  { prompt: 'Business portrait' }
);
```
