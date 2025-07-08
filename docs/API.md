# Freepik AI Orchestrator API Documentation

## Overview

The Freepik AI Orchestrator provides a comprehensive API for AI-powered image generation with LLM optimization. This document outlines the available endpoints and their usage.

## Authentication

All API endpoints require authentication using an API key:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Base URL

```
https://api.freepik-orchestrator.com/v1
```

## Endpoints

### Image Generation

#### Generate Image
Generate an image using the optimized workflow.

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
  "prompt": "Professional headshot of a businesswoman",
  "model": "auto",
  "style": "photorealistic",
  "aspect_ratio": "16:9",
  "quality_level": 8,
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_12345",
  "model_used": "imagen3",
  "status": "pending",
  "estimated_completion": "30-60 seconds",
  "webhook_callback": true
}
```

#### Check Generation Status
Check the status of a generation task.

**Endpoint:** `GET /generate/{task_id}`

**Response:**
```json
{
  "task_id": "task_12345",
  "status": "completed",
  "image_url": "https://cdn.freepik.com/result.jpg",
  "thumbnail_url": "https://cdn.freepik.com/thumb.jpg",
  "model_used": "imagen3",
  "processing_time": 45,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:45Z"
}
```

### Workflow Management

#### Execute Workflow
Execute a predefined workflow.

**Endpoint:** `POST /workflows/{workflow_id}/execute`

**Request Body:**
```json
{
  "prompt": "Professional headshot of a businesswoman",
  "custom_params": {
    "upscale_factor": 4,
    "lighting_style": "professional"
  }
}
```

**Response:**
```json
{
  "workflow_execution_id": "exec_67890",
  "workflow_name": "professional_headshot",
  "status": "running",
  "estimated_completion": "3-4 minutes",
  "steps": [
    {
      "step": 1,
      "action": "generate",
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
