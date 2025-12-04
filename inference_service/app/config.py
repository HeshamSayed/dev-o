"""
Configuration management for AI Inference Service
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 7000
    
    # Model configuration
    MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.2"
    DEVICE: str = "cuda"  # cuda or cpu
    
    # Token limits
    MAX_INPUT_TOKENS: int = 4096
    MAX_OUTPUT_TOKENS: int = 2048
    
    # Quantization (memory optimization)
    LOAD_IN_4BIT: bool = False
    LOAD_IN_8BIT: bool = False
    
    # API configuration
    API_KEY: Optional[str] = None  # Optional API key for authentication
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
