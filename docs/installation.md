# Installation Guide

This guide will walk you through setting up the Freepik AI Orchestrator on your local machine or server.

## Prerequisites

Before installing the Freepik AI Orchestrator, ensure you have the following prerequisites:

### System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 2GB free disk space

### API Keys Required

You'll need the following API keys to use the platform:

1. **Freepik API Key** - Get it from [Freepik Developer Portal](https://freepik.com/api)
2. **LLM API Key** - One of the following:
   - OpenAI API Key (recommended)
   - Anthropic API Key
   - Other compatible LLM provider

## Installation Methods

Choose the installation method that best fits your needs:

=== "Local Installation"

    ### Step 1: Clone the Repository

    ```bash
    git clone https://github.com/yourusername/freepik-ai-orchestrator.git
    cd freepik-ai-orchestrator
    ```

    ### Step 2: Create Virtual Environment

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

    ### Step 3: Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

    ### Step 4: Set Up Environment Variables

    ```bash
    # Copy the example environment file
    cp .env.example .env

    # Edit the .env file with your API keys
    # Use your preferred text editor
    nano .env  # or vim .env or code .env
    ```

    ### Step 5: Initialize Database

    ```bash
    python -c "from database.db import init_db; init_db()"
    ```

    ### Step 6: Run the Application

    ```bash
    streamlit run app.py
    ```

=== "Docker Installation"

    ### Step 1: Clone the Repository

    ```bash
    git clone https://github.com/yourusername/freepik-ai-orchestrator.git
    cd freepik-ai-orchestrator
    ```

    ### Step 2: Set Up Environment Variables

    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```

    ### Step 3: Build and Run with Docker Compose

    ```bash
    docker-compose up --build
    ```

    The application will be available at `http://localhost:8501`

=== "Development Setup"

    ### Step 1: Clone and Setup

    ```bash
    git clone https://github.com/yourusername/freepik-ai-orchestrator.git
    cd freepik-ai-orchestrator
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

    ### Step 2: Install Development Dependencies

    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # Additional dev tools
    ```

    ### Step 3: Install Pre-commit Hooks

    ```bash
    pre-commit install
    ```

    ### Step 4: Run Tests

    ```bash
    pytest tests/
    ```

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Freepik API Configuration
FREEPIK_API_KEY=your_freepik_api_key_here
FREEPIK_BASE_URL=https://api.freepik.com

# LLM Configuration (choose one)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Application Configuration
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=sqlite:///freepik_orchestrator.db

# Webhook Configuration (optional)
WEBHOOK_URL=https://your-webhook-url.com/webhook
WEBHOOK_SECRET=your_webhook_secret

# UI Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Verification

After installation, verify that everything is working correctly:

### 1. Check Application Startup

Navigate to `http://localhost:8501` in your browser. You should see the Freepik AI Orchestrator interface.

### 2. Test API Connection

In the application interface:
1. Try generating a simple image with a basic prompt
2. Check that the LLM optimization is working
3. Verify that images are being generated successfully

### 3. Run Health Check

```bash
# If running locally
curl http://localhost:8501/health

# Should return status 200 with application info
```

## Troubleshooting

### Common Issues

#### Port Already in Use

If port 8501 is already in use:

```bash
# Find the process using the port
netstat -tulpn | grep 8501

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or run on a different port
streamlit run app.py --server.port 8502
```

#### API Key Issues

1. **Freepik API Key Invalid**: Verify your key at the Freepik Developer Portal
2. **LLM API Key Invalid**: Check your OpenAI/Anthropic dashboard
3. **Rate Limits**: Ensure you have sufficient API quota

#### Dependencies Issues

```bash
# Clear pip cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
```

#### Database Issues

```bash
# Reset database
rm freepik_orchestrator.db
python -c "from database.db import init_db; init_db()"
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search existing [GitHub Issues](https://github.com/yourusername/freepik-ai-orchestrator/issues)
3. Create a new issue with detailed error information
4. Join our [Discord Community](https://discord.gg/freepik-ai) for real-time help

## Next Steps

Now that you have the Freepik AI Orchestrator installed:

1. **Configuration**: Review the [Configuration Guide](configuration.md)
2. **Quick Start**: Follow the [Quick Start Tutorial](quickstart.md)
3. **Usage**: Learn about [Features and Usage](usage.md)

Congratulations! You're ready to start generating amazing images with AI! 🎉
