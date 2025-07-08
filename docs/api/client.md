# API Client Reference

This page provides comprehensive documentation for the Freepik AI Orchestrator API client libraries and usage patterns.

## Python Client

### Installation

```python
pip install freepik-ai-orchestrator-client
```

### Basic Usage

```python
from freepik_ai_orchestrator import OrchestrationClient

# Initialize client
client = OrchestrationClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)

# Generate content
response = client.generate(
    prompt="A beautiful sunset over mountains",
    model="dall-e-3",
    style="photorealistic"
)

print(f"Generated image URL: {response.image_url}")
```

### Client Configuration

```python
client = OrchestrationClient(
    base_url="https://your-domain.com",
    api_key="your-api-key",
    timeout=30,
    max_retries=3,
    retry_backoff=2.0
)
```

### Authentication

#### API Key Authentication

```python
client = OrchestrationClient(
    base_url="http://localhost:8000",
    api_key="sk-your-api-key-here"
)
```

#### Bearer Token Authentication

```python
client = OrchestrationClient(
    base_url="http://localhost:8000",
    bearer_token="your-bearer-token"
)
```

## API Methods

### Content Generation

#### `generate()`

Generate AI content using various models.

```python
response = client.generate(
    prompt="Your creative prompt",
    model="dall-e-3",
    style="photorealistic",
    size="1024x1024",
    quality="hd",
    metadata={
        "campaign": "summer-2024",
        "brand": "your-brand"
    }
)
```

**Parameters:**
- `prompt` (str): The text prompt for generation
- `model` (str): Model to use (dall-e-3, midjourney, stable-diffusion, etc.)
- `style` (str, optional): Art style preference
- `size` (str, optional): Output dimensions
- `quality` (str, optional): Quality setting
- `metadata` (dict, optional): Additional metadata

**Returns:**
- `GenerationResponse` object with image URLs, metadata, and analytics

#### `generate_batch()`

Generate multiple variations or images in a single request.

```python
responses = client.generate_batch(
    prompts=["Prompt 1", "Prompt 2", "Prompt 3"],
    model="dall-e-3",
    batch_size=3
)
```

### Model Management

#### `list_models()`

Get available AI models and their capabilities.

```python
models = client.list_models()
for model in models:
    print(f"{model.name}: {model.description}")
```

#### `get_model_info()`

Get detailed information about a specific model.

```python
model_info = client.get_model_info("dall-e-3")
print(f"Max resolution: {model_info.max_resolution}")
print(f"Supported styles: {model_info.supported_styles}")
```

### Analytics and Monitoring

#### `get_usage_stats()`

Retrieve usage statistics and analytics.

```python
stats = client.get_usage_stats(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
print(f"Total generations: {stats.total_generations}")
print(f"Cost: ${stats.total_cost}")
```

#### `get_generation_history()`

Get history of past generations.

```python
history = client.get_generation_history(
    limit=50,
    filter_by_model="dall-e-3"
)
```

## Response Objects

### GenerationResponse

```python
class GenerationResponse:
    id: str                    # Unique generation ID
    image_url: str            # Generated image URL
    thumbnail_url: str        # Thumbnail URL
    prompt: str               # Original prompt
    model: str                # Model used
    style: str                # Style applied
    size: str                 # Image dimensions
    quality: str              # Quality setting
    metadata: dict            # Additional metadata
    created_at: datetime      # Generation timestamp
    processing_time: float    # Time taken to generate
    cost: float               # Cost of generation
```

### ModelInfo

```python
class ModelInfo:
    name: str                 # Model name
    description: str          # Model description
    max_resolution: str       # Maximum supported resolution
    supported_styles: list    # Available styles
    pricing_per_image: float  # Cost per generation
    average_time: float       # Average processing time
```

## Error Handling

```python
from freepik_ai_orchestrator.exceptions import (
    OrchestrationError,
    AuthenticationError,
    RateLimitError,
    ModelNotAvailableError
)

try:
    response = client.generate(
        prompt="Beautiful landscape",
        model="dall-e-3"
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after}")
except ModelNotAvailableError:
    print("Requested model is not available")
except OrchestrationError as e:
    print(f"Generation failed: {e.message}")
```

## Async Client

For high-throughput applications, use the async client:

```python
import asyncio
from freepik_ai_orchestrator import AsyncOrchestrationClient

async def generate_async():
    client = AsyncOrchestrationClient(
        base_url="http://localhost:8000",
        api_key="your-api-key"
    )
    
    response = await client.generate(
        prompt="Async generation test",
        model="dall-e-3"
    )
    
    await client.close()
    return response

# Run async generation
response = asyncio.run(generate_async())
```

## JavaScript/TypeScript Client

### Installation

```bash
npm install @freepik/ai-orchestrator-client
```

### Basic Usage

```javascript
import { OrchestrationClient } from '@freepik/ai-orchestrator-client';

const client = new OrchestrationClient({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your-api-key'
});

// Generate content
const response = await client.generate({
  prompt: 'A beautiful sunset over mountains',
  model: 'dall-e-3',
  style: 'photorealistic'
});

console.log('Generated image URL:', response.imageUrl);
```

### TypeScript Types

```typescript
interface GenerationRequest {
  prompt: string;
  model: string;
  style?: string;
  size?: string;
  quality?: string;
  metadata?: Record<string, any>;
}

interface GenerationResponse {
  id: string;
  imageUrl: string;
  thumbnailUrl: string;
  prompt: string;
  model: string;
  style: string;
  size: string;
  quality: string;
  metadata: Record<string, any>;
  createdAt: Date;
  processingTime: number;
  cost: number;
}
```

## cURL Examples

### Generate Image

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "model": "dall-e-3",
    "style": "photorealistic",
    "size": "1024x1024"
  }'
```

### List Models

```bash
curl -X GET "http://localhost:8000/api/v1/models" \
  -H "Authorization: Bearer your-api-key"
```

### Get Generation History

```bash
curl -X GET "http://localhost:8000/api/v1/generations?limit=10" \
  -H "Authorization: Bearer your-api-key"
```

## Best Practices

### 1. Connection Pooling

Use connection pooling for better performance:

```python
client = OrchestrationClient(
    base_url="http://localhost:8000",
    api_key="your-api-key",
    max_connections=10,
    keep_alive=True
)
```

### 2. Retry Logic

Implement exponential backoff for retries:

```python
import time
import random

def generate_with_retry(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.generate(prompt=prompt, model="dall-e-3")
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
```

### 3. Batch Processing

Use batch processing for multiple generations:

```python
# Process multiple prompts efficiently
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
responses = client.generate_batch(prompts=prompts, model="dall-e-3")
```

### 4. Resource Cleanup

Always clean up resources:

```python
try:
    response = client.generate(prompt="Test", model="dall-e-3")
finally:
    client.close()
```

## Client Libraries

| Language | Package | Repository |
|----------|---------|------------|
| Python | `freepik-ai-orchestrator-client` | [GitHub](https://github.com/freepik/ai-orchestrator-python) |
| JavaScript/TypeScript | `@freepik/ai-orchestrator-client` | [GitHub](https://github.com/freepik/ai-orchestrator-js) |
| PHP | `freepik/ai-orchestrator-php` | [GitHub](https://github.com/freepik/ai-orchestrator-php) |
| Ruby | `freepik-ai-orchestrator` | [GitHub](https://github.com/freepik/ai-orchestrator-ruby) |

## Support

For client-specific issues:
- Check the [API documentation](../API.md)
- Review [troubleshooting guide](../troubleshooting.md)
- Open an issue on the respective client library repository
