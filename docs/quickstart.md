# Quick Start Tutorial

Get up and running with the Freepik AI Orchestrator in just a few minutes! This tutorial will guide you through your first image generation.

## Prerequisites

Before starting this tutorial, make sure you have:

- Completed the [Installation](installation.md)
- Configured your [API keys](configuration.md)
- Application running at `http://localhost:8501`

## Your First Image Generation

### Step 1: Access the Application

Open your web browser and navigate to:
```
http://localhost:8501
```

You should see the Freepik AI Orchestrator welcome screen.

### Step 2: Enter a Basic Prompt

In the main interface:

1. Locate the **"Prompt"** text area
2. Enter a simple prompt like:
   ```
   A beautiful sunset over a mountain lake
   ```

### Step 3: Choose Your Model

1. Find the **"Model Selection"** dropdown
2. For your first generation, choose **"Classic Fast"** (fastest option)
3. Keep other settings at their defaults for now

### Step 4: Generate Your Image

1. Click the **"Generate Image"** button
2. Watch as the LLM optimizes your prompt
3. Wait for the image generation to complete (usually 10-30 seconds)

### Step 5: View Your Results

Once generation is complete, you'll see:

- **Original Prompt**: Your input
- **Optimized Prompt**: LLM-enhanced version
- **Generated Image**: Your AI-created artwork
- **Metadata**: Generation details and statistics

## Exploring Features

Now that you've generated your first image, let's explore more features:

### LLM Prompt Optimization

The platform automatically enhances your prompts. Try these examples:

#### Basic Prompt
```
dog in park
```

#### LLM-Optimized Result
```
A friendly golden retriever playing in a sunny park with green grass, 
tall trees in the background, natural lighting, high quality photography, 
vibrant colors, joyful atmosphere
```

### Model Comparison

Try the same prompt with different models:

1. **Classic Fast**: Quick results, good for testing
2. **Flux Dev**: Balanced speed and quality
3. **Imagen3**: High quality, slower generation
4. **Mystic**: Artistic style, premium quality

### Advanced Settings

Experiment with these settings:

#### Image Dimensions
- **Square**: 1024x1024 (default)
- **Portrait**: 768x1024
- **Landscape**: 1024x768
- **Custom**: Set your own dimensions

#### Style Parameters
- **Artistic Style**: Realistic, Artistic, Cartoon, etc.
- **Color Palette**: Vibrant, Muted, Monochrome
- **Lighting**: Natural, Dramatic, Soft

#### Post-Processing
- **Upscaling**: Increase resolution
- **Background Removal**: Isolate subjects
- **Style Transfer**: Apply artistic filters

## Step-by-Step Walkthrough

Let's create a more complex image with advanced features:

### Step 1: Advanced Prompt
```
A cyberpunk city at night with neon lights
```

### Step 2: Model Selection
Choose **"Imagen3"** for high quality

### Step 3: Configure Settings
- **Dimensions**: 1024x768 (landscape)
- **Style**: Sci-fi/Futuristic
- **Lighting**: Dramatic
- **Color Palette**: Vibrant neons

### Step 4: Enable Post-Processing
- Check **"Enhance Resolution"**
- Select **"Dramatic Lighting"** filter

### Step 5: Generate and Review
1. Click **"Generate Image"**
2. Review the optimized prompt
3. Examine the generated image
4. Check the analytics panel

## Understanding the Interface

### Main Sections

#### 1. Prompt Input Area
- **Text Area**: Enter your image description
- **Enhance Button**: Manually trigger LLM optimization
- **Prompt History**: Access previous prompts

#### 2. Model & Settings Panel
- **Model Selector**: Choose AI model
- **Dimension Controls**: Set image size
- **Style Options**: Customize appearance
- **Advanced Settings**: Fine-tune parameters

#### 3. Generation Controls
- **Generate Button**: Start image creation
- **Stop Button**: Cancel ongoing generation
- **Queue Status**: View generation progress

#### 4. Results Area
- **Image Display**: View generated images
- **Metadata Panel**: Generation details
- **Download Options**: Save images
- **Share Controls**: Export or share results

#### 5. Analytics Dashboard
- **Usage Statistics**: Track your generations
- **Cost Tracking**: Monitor API usage
- **Performance Metrics**: Generation times and success rates

### Navigation Tips

#### Sidebar Menu
- **Dashboard**: Main generation interface
- **Gallery**: View all generated images
- **Analytics**: Detailed statistics
- **Settings**: Configure preferences
- **Help**: Documentation and support

#### Keyboard Shortcuts
- `Ctrl + Enter`: Generate image
- `Ctrl + S`: Save current image
- `Ctrl + H`: Show/hide help panel
- `Esc`: Cancel generation

## Best Practices

### Writing Effective Prompts

#### Be Descriptive
**Good**: "A majestic white horse galloping through a field of wildflowers at sunset"
**Bad**: "horse running"

#### Include Style Information
**Good**: "Portrait photo of a person, professional lighting, studio quality"
**Bad**: "person photo"

#### Specify Technical Details
**Good**: "High resolution, 4K quality, detailed textures, photorealistic"
**Bad**: "good quality"

### Model Selection Guide

#### When to Use Each Model

**Classic Fast**
- Quick tests and iterations
- Simple images
- Development and prototyping

**Flux Dev**
- Balanced quality and speed
- General purpose generation
- Medium complexity images

**Imagen3**
- High-quality results needed
- Complex scenes
- Final production images

**Mystic**
- Artistic and creative styles
- Unique aesthetic requirements
- Premium quality outputs

### Optimization Tips

#### Prompt Engineering
1. Start simple, then add details
2. Use the LLM optimization feature
3. Study the optimized prompts to learn
4. Build a library of effective prompts

#### Workflow Efficiency
1. Use prompt history for similar requests
2. Save successful configurations
3. Batch similar generations
4. Monitor usage to optimize costs

## Common Use Cases

### Marketing Materials
```
Professional product photography of a smartphone on a clean white background, 
studio lighting, high resolution, commercial quality
```

### Social Media Content
```
Vibrant lifestyle photo of friends having coffee in a modern café, 
natural lighting, candid moment, Instagram-style
```

### Concept Art
```
Fantasy landscape with floating islands, magical waterfalls, 
ethereal lighting, digital art style, highly detailed
```

### Business Presentations
```
Modern office meeting room with diverse team collaborating, 
professional atmosphere, clean and minimal design
```

## Troubleshooting Quick Issues

### Generation Fails
1. Check your API key configuration
2. Verify internet connection
3. Try a simpler prompt
4. Switch to a different model

### Slow Performance
1. Use "Classic Fast" for testing
2. Reduce image dimensions
3. Simplify post-processing options
4. Check server load in analytics

### Poor Quality Results
1. Use more descriptive prompts
2. Try LLM optimization
3. Switch to higher-quality models
4. Adjust style parameters

### Interface Issues
1. Refresh the browser page
2. Clear browser cache
3. Try a different browser
4. Check browser console for errors

## Next Steps

Congratulations! You've successfully generated your first images with the Freepik AI Orchestrator. Here's what to explore next:

### Learn More
- [Detailed Usage Guide](USAGE.md): Comprehensive feature documentation
- [API Reference](API.md): Technical integration details
- [Configuration](configuration.md): Advanced setup options

### Advanced Features
- **Batch Processing**: Generate multiple images at once
- **Webhook Integration**: Automate workflows
- **Custom Models**: Train and deploy your own models
- **API Integration**: Embed in your applications

### Get Involved
- [Contributing Guide](development/contributing.md): Help improve the platform
- [GitHub Issues](https://github.com/yourusername/freepik-ai-orchestrator/issues): Report bugs or request features
- [Discord Community](https://discord.gg/freepik-ai): Connect with other users

Happy generating! 🎨✨
