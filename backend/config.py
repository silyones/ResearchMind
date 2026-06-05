from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str
    tavily_api_key: str
    langsmith_api_key: str
    
    # Model Configuration
    model_name: str = Field(default="llama-3.1-8b-instant", validation_alias="MODEL_NAME")
    model_name_llm: str = Field(default="llama-3.1-8b-instant", validation_alias="MODEL_NAME_LLM")
    max_search_results: int = 5
    max_agent_iterations: int = 10
    
    # LangSmith Configuration
    langsmith_tracing: bool = False
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langchain_project: str = "research_mind"
    
    # FastAPI Configuration
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    
    # Runtime Configuration
    streaming: bool = True
    request_timeout: int = 60
    log_level: str = "INFO"
    env: str = "development"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "protected_namespaces": ("settings_",),
    }


# Global settings instance
settings = Settings()

