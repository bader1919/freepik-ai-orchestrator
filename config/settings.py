import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FreepikConfig:
    api_key: str
    webhook_secret: str
    base_url: str = "https://api.freepik.com"
    webhook_url: str = ""
    environment: str = "development"

@dataclass
class LLMConfig:
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.3

@dataclass
class DatabaseConfig:
    url: str
    echo: bool = False

@dataclass
class AppConfig:
    secret_key: str
    debug: bool = False
    log_level: str = "INFO"

def get_config():
    """Get application configuration"""
    environment = os.getenv("ENVIRONMENT", "development")
    webhook_base = os.getenv("FREEPIK_WEBHOOK_URL", "https://localhost:8501/webhook")
    
    return {
        "freepik": FreepikConfig(
            api_key=os.getenv("FREEPIK_API_KEY", ""),
            webhook_secret=os.getenv("FREEPIK_WEBHOOK_SECRET", ""),
            webhook_url=f"{webhook_base}/freepik",
            environment=environment
        ),
        "llm": LLMConfig(
            openai_key=os.getenv("OPENAI_API_KEY"),
            anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("LLM_MODEL", "gpt-4")
        ),
        "database": DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///freepik_orchestrator.db"),
            echo=os.getenv("DEBUG", "False").lower() == "true"
        ),
        "app": AppConfig(
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key"),
            debug=os.getenv("DEBUG", "False").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
    }

# Global config instance
CONFIG = get_config()
