# Core API Reference

Technical reference for the core modules and classes of the Freepik AI Orchestrator.

## Core Modules

### `core.llm_orchestrator`

The main orchestrator that handles LLM-powered prompt enhancement and model selection.

#### Class: `LLMOrchestrator`

**Description**: Main class for orchestrating LLM interactions and prompt optimization.

**Constructor**:
```python
LLMOrchestrator(
    provider: str = "openai",
    model: str = "gpt-4",
    temperature: float = 0.7
)
```

**Parameters**:
- `provider` (str): LLM provider ("openai" or "anthropic")
- `model` (str): Specific model to use
- `temperature` (float): Creativity level (0.0-1.0)

**Methods**:

##### `enhance_prompt(prompt: str) -> str`

Enhance a user prompt with LLM optimization.

**Parameters**:
- `prompt` (str): Original user prompt

**Returns**:
- `str`: Enhanced prompt with technical and artistic details

**Example**:
```python
orchestrator = LLMOrchestrator()
enhanced = orchestrator.enhance_prompt("business headshot")
print(enhanced)
# Output: "Professional business headshot of a person, confident expression..."
```

##### `select_optimal_model(prompt: str, requirements: dict) -> str`

Automatically select the best AI model for a given prompt.

**Parameters**:
- `prompt` (str): Enhanced prompt text
- `requirements` (dict): Generation requirements (quality, speed, style)

**Returns**:
- `str`: Recommended model name

**Example**:
```python
model = orchestrator.select_optimal_model(
    prompt="Professional headshot...",
    requirements={"quality": "high", "style": "photorealistic"}
)
print(model)  # Output: "imagen3"
```

### `core.freepik_client`

Client for interacting with the Freepik API.

#### Class: `FreepikClient`

**Description**: Handles all interactions with the Freepik API for image generation.

**Constructor**:
```python
FreepikClient(
    api_key: str,
    base_url: str = "https://api.freepik.com",
    timeout: int = 30
)
```

**Parameters**:
- `api_key` (str): Freepik API key
- `base_url` (str): API base URL
- `timeout` (int): Request timeout in seconds

**Methods**:

##### `generate_image(prompt: str, **kwargs) -> dict`

Generate an image using the Freepik API.

**Parameters**:
- `prompt` (str): Image description
- `model` (str, optional): AI model to use
- `aspect_ratio` (str, optional): Image dimensions
- `quality_level` (int, optional): Quality setting (1-10)

**Returns**:
- `dict`: Generation response with task_id and status

**Example**:
```python
client = FreepikClient(api_key="your_key")
result = client.generate_image(
    prompt="Professional headshot",
    model="imagen3",
    quality_level=9
)
```

##### `get_generation_status(task_id: str) -> dict`

Check the status of a generation task.

**Parameters**:
- `task_id` (str): Task identifier from generation request

**Returns**:
- `dict`: Task status and results

##### `download_image(image_url: str, save_path: str) -> str`

Download generated image to local filesystem.

**Parameters**:
- `image_url` (str): URL of generated image
- `save_path` (str): Local path to save image

**Returns**:
- `str`: Path to saved image file

### `core.post_processor`

Post-processing utilities for image enhancement.

#### Class: `PostProcessor`

**Description**: Handles image post-processing operations like upscaling and enhancement.

**Methods**:

##### `upscale_image(image_path: str, scale_factor: int = 2) -> str`

Upscale an image using AI enhancement.

**Parameters**:
- `image_path` (str): Path to input image
- `scale_factor` (int): Scaling factor (2 or 4)

**Returns**:
- `str`: Path to upscaled image

##### `remove_background(image_path: str) -> str`

Remove background from an image.

**Parameters**:
- `image_path` (str): Path to input image

**Returns**:
- `str`: Path to image with removed background

##### `apply_relighting(image_path: str, style: str = "professional") -> str`

Apply lighting effects to an image.

**Parameters**:
- `image_path` (str): Path to input image
- `style` (str): Lighting style ("professional", "dramatic", "natural")

**Returns**:
- `str`: Path to relit image

## Configuration Classes

### `config.settings`

#### Class: `Settings`

**Description**: Application configuration management using Pydantic.

**Attributes**:
- `freepik_api_key` (str): Freepik API key
- `openai_api_key` (str, optional): OpenAI API key
- `anthropic_api_key` (str, optional): Anthropic API key
- `database_url` (str): Database connection string
- `redis_url` (str, optional): Redis connection string
- `environment` (str): Environment name ("development", "production")
- `debug` (bool): Debug mode flag

**Example**:
```python
from config.settings import Settings

settings = Settings()
print(settings.freepik_api_key)
```

## Database Models

### `database.models`

#### Class: `Generation`

**Description**: Database model for image generation records.

**Fields**:
- `id` (int): Primary key
- `task_id` (str): Unique task identifier
- `user_id` (str): User identifier
- `original_prompt` (str): User's original prompt
- `enhanced_prompt` (str): LLM-enhanced prompt
- `model_used` (str): AI model used for generation
- `status` (str): Generation status
- `image_url` (str, optional): URL of generated image
- `created_at` (datetime): Creation timestamp
- `completed_at` (datetime, optional): Completion timestamp

**Methods**:

##### `create(cls, **kwargs) -> Generation`

Create a new generation record.

##### `get_by_task_id(cls, task_id: str) -> Generation`

Retrieve generation by task ID.

##### `update_status(self, status: str, **kwargs) -> None`

Update generation status and related fields.

## Utility Functions

### `utils.prompt_templates`

#### Function: `get_template(category: str) -> str`

Get a prompt template for a specific category.

**Parameters**:
- `category` (str): Template category ("business", "artistic", "product")

**Returns**:
- `str`: Prompt template string

**Example**:
```python
from utils.prompt_templates import get_template

template = get_template("business")
prompt = template.format(subject="headshot", style="professional")
```

### `utils.image_utils`

#### Function: `validate_image_url(url: str) -> bool`

Validate if a URL points to a valid image.

#### Function: `get_image_dimensions(image_path: str) -> tuple`

Get image dimensions.

**Returns**:
- `tuple`: (width, height) in pixels

#### Function: `optimize_image_size(image_path: str, max_size_mb: int = 10) -> str`

Optimize image file size while maintaining quality.

## Error Classes

### `exceptions.FreepikOrchestratorError`

Base exception class for all application errors.

### `exceptions.APIError`

Raised when API requests fail.

**Attributes**:
- `status_code` (int): HTTP status code
- `error_code` (str): Application error code
- `message` (str): Error message

### `exceptions.GenerationError`

Raised when image generation fails.

### `exceptions.ConfigurationError`

Raised when configuration is invalid or missing.

## Usage Examples

### Complete Generation Workflow

```python
from core.llm_orchestrator import LLMOrchestrator
from core.freepik_client import FreepikClient
from core.post_processor import PostProcessor

# Initialize components
orchestrator = LLMOrchestrator()
client = FreepikClient(api_key="your_key")
processor = PostProcessor()

# Generate image
prompt = "business headshot"
enhanced_prompt = orchestrator.enhance_prompt(prompt)
model = orchestrator.select_optimal_model(enhanced_prompt, {"quality": "high"})

result = client.generate_image(
    prompt=enhanced_prompt,
    model=model
)

# Wait for completion (in practice, use webhooks)
import time
while True:
    status = client.get_generation_status(result["task_id"])
    if status["status"] == "completed":
        break
    time.sleep(5)

# Download and process
image_path = client.download_image(
    status["image_url"], 
    "output/generated_image.jpg"
)

# Apply post-processing
upscaled_path = processor.upscale_image(image_path, scale_factor=2)
relit_path = processor.apply_relighting(upscaled_path, style="professional")
```

### Async Generation with Webhooks

```python
import asyncio
from core.llm_orchestrator import LLMOrchestrator
from core.freepik_client import FreepikClient

async def generate_with_webhook():
    orchestrator = LLMOrchestrator()
    client = FreepikClient(api_key="your_key")
    
    enhanced_prompt = orchestrator.enhance_prompt("mountain landscape")
    
    result = client.generate_image(
        prompt=enhanced_prompt,
        webhook_url="https://your-app.com/webhook"
    )
    
    print(f"Generation started: {result['task_id']}")
    return result["task_id"]

# Webhook handler (Flask example)
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if data['event'] == 'generation.completed':
        print(f"Generation {data['data']['task_id']} completed!")
        print(f"Image URL: {data['data']['image_url']}")
    return "OK"
```

For more detailed examples and advanced usage patterns, see the [Usage Guide](../USAGE.md) and [API Reference](../API.md).
