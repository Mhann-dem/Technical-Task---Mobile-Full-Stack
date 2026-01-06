"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # File upload settings
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png"]
    
    # API settings
    API_KEY_HEADER: str = "X-API-Key"
    ENABLE_API_KEY: bool = True
    API_KEY: Optional[str] = os.getenv("API_KEY", "test-api-key-12345")
    
    # Analysis settings
    CONFIDENCE_THRESHOLD: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
