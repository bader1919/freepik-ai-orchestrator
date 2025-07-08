# 🎨 Freepik AI Orchestrator

Professional AI-powered image generation platform with LLM optimization for Freepik API. Built with Streamlit for beautiful, interactive user experience.

## ✨ Features

- **🤖 LLM-Powered Prompt Engineering** - Automatically optimizes prompts for better results
- **🎯 Multi-Model Support** - Mystic, Imagen3, Flux Dev, Classic Fast
- **🔄 Post-Processing Pipelines** - Upscaling, relighting, style transfer, background removal
- **📊 Real-time Analytics** - Track usage, success rates, and costs
- **🎨 Professional UI** - Clean Streamlit interface with custom styling
- **⚡ Async Processing** - Webhook-based result handling
- **🔒 Production Ready** - Docker support, environment management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Freepik API key
- OpenAI/Anthropic API key (for LLM optimization)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables

```bash
# Freepik API
FREEPIK_API_KEY=your_freepik_api_key
FREEPIK_WEBHOOK_SECRET=your_webhook_secret
FREEPIK_WEBHOOK_URL=https://your-domain.com/webhook

# LLM Configuration
OPENAI_API_KEY=your_openai_key
# OR
ANTHROPIC_API_KEY=your_claude_key

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Environment
ENVIRONMENT=development
```

## 📖 Usage

### Basic Generation
1. Enter your image description
2. Select preferences (model, style, aspect ratio)
3. Click "Generate Image"
4. AI optimizes your prompt and selects the best model
5. Receive results via webhook or real-time updates

### Advanced Workflows
- **Professional Headshots**: Generate → Relight → Upscale
- **Product Photography**: Generate → Remove Background → Multiple Angles
- **Marketing Materials**: Generate → Style Variations → Brand Overlay

## 🏗️ Architecture

```
User Input → LLM Optimizer → Model Selection → Freepik API → Webhook → Post-Processing → Results
```

### Supported Models
- **Mystic**: Freepik's balanced model for general use
- **Imagen3**: Google's photorealistic model
- **Flux Dev**: Advanced artistic control
- **Classic Fast**: Quick iterations

## 🚢 Deployment

### Docker
```bash
docker build -t freepik-orchestrator .
docker run -p 8501:8501 freepik-orchestrator
```

### Docker Compose
```bash
docker-compose up -d
```

### Streamlit Cloud
1. Push to GitHub
2. Connect via [streamlit.io](https://streamlit.io)
3. Deploy with environment variables

## 📊 Business Model

### Pricing Tiers
- **Free**: 10 generations/day
- **Professional**: Unlimited generations, priority support
- **Enterprise**: Custom workflows, white-label options

### Revenue Streams
- SaaS subscriptions
- Custom implementations
- Training and consulting
- API access licensing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@yourcompany.com
- 💬 Discord: [Join our community](https://discord.gg/yourserver)
- 📖 Documentation: [Full docs](./docs/)

## 🙏 Acknowledgments

- [Freepik](https://freepik.com) for their amazing API
- [Streamlit](https://streamlit.io) for the beautiful UI framework
- [OpenAI](https://openai.com) for LLM capabilities

---

**Built with ❤️ for the AI generation community**