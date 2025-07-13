from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Workforce Distribution.ai"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./workforce_ai.db")
    
    # Security settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    # CORS settings
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8501"]
    
    # AI/ML settings
    model_path: str = "models/"
    skills_threshold: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings() 