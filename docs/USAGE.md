# Usage Guide

This guide provides comprehensive instructions for using the Freepik AI Orchestrator platform.

## Getting Started

### 1. Account Setup

1. **Sign up** for an account at [freepik-orchestrator.com](https://freepik-orchestrator.com)
2. **Verify your email** address
3. **Choose your plan**: Free, Professional, or Enterprise
4. **Get your API key** from the dashboard

### 2. First Image Generation

1. **Open the application** in your browser
2. **Enter your prompt** in the main text area
3. **Select preferences** (optional)
4. **Click "Generate Image"**
5. **Wait for results** (30-60 seconds for most models)

## User Interface Guide

### Main Dashboard

The dashboard provides access to all major features:

- **Generate Tab**: Create new images
- **Analytics Tab**: View usage statistics
- **Workflows Tab**: Access predefined workflows
- **Settings Tab**: Configure preferences

### Generation Interface

#### Prompt Input
- **Main prompt area**: Describe your desired image
- **Quick templates**: Use predefined prompts for common use cases
- **Enhancement studio**: Access advanced prompt optimization tools

#### Preferences Panel
- **Model selection**: Choose specific AI models or use auto-selection
- **Style preferences**: Set artistic direction
- **Quality settings**: Adjust output quality and creativity levels
- **Aspect ratio**: Select image dimensions

#### Results Panel
- **Image gallery**: View generated images
- **Download options**: Save images in various formats
- **Post-processing**: Access upscaling and enhancement tools
- **Metadata**: View generation details and settings

## Core Features

### Prompt Engineering

The platform automatically optimizes your prompts using AI:

#### Basic Prompts
```
Input: "business headshot"
Enhanced: "Professional business headshot, confident expression, modern office background, natural lighting, shot with Canon 5D Mark IV, 85mm lens, sharp focus, high resolution"
```

#### Style Enhancement
```
Input: "cat painting"
Enhanced: "Digital art painting of a cat, artistic brush strokes, vibrant colors, detailed fur texture, creative composition, high resolution illustration"
```

### Model Selection

#### Auto-Selection (Recommended)
Let AI choose the optimal model based on your prompt:
- Analyzes prompt content and style requirements
- Considers use case (professional, artistic, commercial)
- Selects best model for quality and speed

#### Manual Selection
Choose specific models for particular needs:

- **Mystic**: Balanced general-purpose model
  - Best for: Mixed content, versatile applications
  - Speed: Medium (30-45 seconds)
  - Quality: High

- **Imagen3**: Photorealistic model
  - Best for: Professional photos, portraits, products
  - Speed: Medium (45-60 seconds)
  - Quality: Excellent for realism

- **Flux Dev**: Advanced artistic control
  - Best for: Creative concepts, artistic styles, complex compositions
  - Speed: Slower (60-90 seconds)
  - Quality: Excellent for artistic content

- **Classic Fast**: Quick iterations
  - Best for: Simple requests, rapid prototyping
  - Speed: Fast (10-15 seconds)
  - Quality: Good for basic needs

### Workflows

Pre-built workflows automate complex multi-step processes:

#### Professional Headshots
1. Generate base image with Imagen3
2. Apply professional lighting
3. Upscale to 4K resolution
4. Create lighting variations

**Use for**: LinkedIn profiles, corporate websites, professional portfolios

#### Product Photography
1. Generate product image
2. Remove background
3. Apply studio lighting
4. Create multiple angles
5. Upscale for e-commerce

**Use for**: Online stores, catalogs, marketing materials

#### Marketing Materials
1. Generate base design
2. Create style variations
3. Generate multiple aspect ratios
4. Apply brand overlays

**Use for**: Social media, advertisements, promotional content

### Post-Processing

Enhance generated images with additional AI tools:

#### Upscaling
- **2x Upscale**: Double image resolution
- **4x Upscale**: Quadruple resolution for print quality
- **Smart enhancement**: AI-powered detail improvement

#### Relighting
- **Professional portrait**: Optimized for headshots
- **Studio lighting**: Commercial photography style
- **Natural lighting**: Outdoor/window light effect
- **Dramatic lighting**: Artistic mood lighting

#### Background Tools
- **Remove background**: Create transparent PNG files
- **Replace background**: Swap backgrounds while maintaining subject
- **Blur background**: Create depth-of-field effects

#### Style Transfer
- **Artistic styles**: Apply painting styles (impressionist, abstract, etc.)
- **Photographic styles**: Film styles, vintage effects
- **Brand styles**: Consistent visual identity

## Advanced Usage

### API Integration

Integrate the platform into your applications:

#### Python Example
```python
import requests

api_key = "your-api-key"
headers = {"Authorization": f"Bearer {api_key}"}

# Generate image
response = requests.post(
    "https://api.freepik-orchestrator.com/v1/generate",
    headers=headers,
    json={
        "prompt": "professional headshot",
        "model": "auto",
        "webhook_url": "https://your-app.com/webhook"
    }
)

task_id = response.json()["task_id"]
```

#### JavaScript Example
```javascript
const response = await fetch('https://api.freepik-orchestrator.com/v1/generate', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prompt: 'professional headshot',
    model: 'auto'
  })
});

const result = await response.json();
```

### Webhook Integration

Receive real-time notifications when images are ready:

#### Webhook Setup
1. Provide webhook URL in generation request
2. Verify webhook signature for security
3. Handle different event types

#### Example Webhook Handler (Python)
```python
import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-Freepik-Signature')
    payload = request.get_data()
    
    # Verify signature
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(f"sha256={expected}", signature):
        return "Invalid signature", 401
    
    data = request.json
    if data['event'] == 'generation.completed':
        image_url = data['data']['image_url']
        # Process completed image
        
    return "OK"
```

### Batch Processing

Process multiple images efficiently:

#### Using Workflows
```python
workflow_requests = [
    {"prompt": "CEO headshot", "name": "john_doe"},
    {"prompt": "CTO headshot", "name": "jane_smith"},
    {"prompt": "CFO headshot", "name": "bob_johnson"}
]

for request in workflow_requests:
    response = client.execute_workflow(
        "professional_headshot",
        request["prompt"]
    )
    # Track by name for identification
```

#### Async Processing
```javascript
const promises = prompts.map(prompt => 
    client.generate({
        prompt: prompt,
        webhook_url: 'https://your-app.com/webhook'
    })
);

const results = await Promise.all(promises);
```

## Best Practices

### Prompt Writing

#### Be Specific
```
❌ "person at work"
✅ "professional businesswoman in modern office, confident posture, business attire, natural lighting"
```

#### Include Technical Details
```
❌ "high quality photo"
✅ "shot with Canon 5D Mark IV, 85mm lens, shallow depth of field, professional lighting, sharp focus"
```

#### Specify Style
```
❌ "artistic image"
✅ "digital art illustration, vibrant colors, detailed, concept art style"
```

### Model Selection Guidelines

#### Choose Imagen3 for:
- Professional photography
- Product images
- Realistic portraits
- Commercial content

#### Choose Flux Dev for:
- Artistic illustrations
- Creative concepts
- Complex compositions
- Stylized content

#### Choose Mystic for:
- General purpose needs
- Mixed content types
- Balanced results
- Unknown requirements

#### Choose Classic Fast for:
- Quick iterations
- Simple concepts
- Draft versions
- High-volume processing

### Cost Optimization

#### Use Auto-Selection
Let AI choose the most cost-effective model for your needs.

#### Batch Similar Requests
Group similar prompts to optimize processing.

#### Use Appropriate Quality Settings
Higher quality costs more but provides better results.

#### Cache Common Results
Store frequently used images to avoid regeneration.

### Quality Optimization

#### Iterate on Prompts
Start simple and refine based on results.

#### Use Post-Processing
Enhance results with upscaling and relighting.

#### Compare Models
Test different models for your specific use case.

#### Leverage Workflows
Use predefined workflows for consistent quality.

## Troubleshooting

### Common Issues

#### "Generation Failed" Error
- Check your API key validity
- Verify account has sufficient credits
- Ensure prompt meets content guidelines
- Try a different model if auto-selection fails

#### "Webhook Not Received" Issue
- Verify webhook URL is accessible
- Check webhook signature verification
- Ensure HTTPS is used for webhook URLs
- Test webhook endpoint independently

#### "Poor Quality Results"
- Refine prompt with more specific details
- Try different models for your use case
- Use post-processing to enhance results
- Check quality settings in preferences

#### "Slow Processing Times"
- Consider using Classic Fast for simple requests
- Avoid peak usage hours if possible
- Use async processing with webhooks
- Upgrade to higher tier for priority processing

### Getting Help

#### Support Channels
- **Email**: support@freepik-orchestrator.com
- **Discord**: [Community server](https://discord.gg/freepik-orchestrator)
- **Documentation**: [Full documentation](https://docs.freepik-orchestrator.com)
- **Status Page**: [System status](https://status.freepik-orchestrator.com)

#### Before Contacting Support
- Check the status page for known issues
- Review your API key and account status
- Try the request again with simpler parameters
- Gather error messages and request IDs

## Billing and Limits

### Usage Tracking

Monitor your usage in the Analytics tab:
- **Daily generations**: Track daily usage against limits
- **Model breakdown**: See which models you use most
- **Cost analysis**: Understand spending patterns
- **Success rates**: Monitor generation success rates

### Plan Limits

#### Free Tier
- 10 generations per day
- All models available
- Basic support
- No commercial use

#### Professional Tier
- Unlimited generations
- Priority processing
- Email support
- Commercial use allowed
- Advanced analytics

#### Enterprise Tier
- Volume discounts
- Custom workflows
- Dedicated support
- White-label options
- SLA guarantees

### Upgrade Benefits

Upgrading provides:
- Higher rate limits
- Faster processing
- Better support
- Advanced features
- Commercial usage rights

Ready to get started? Create your account and begin generating amazing AI images with the Freepik AI Orchestrator!
