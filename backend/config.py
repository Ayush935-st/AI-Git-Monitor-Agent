"""
Application configuration.

Loads environment variables from the .env file and provides
a single settings object for the application.
"""

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load the .env file from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):

    app_name: str = "AI Git Monitoring Agent"
    app_version: str = "1.0.0"

    database_url: str

    # Git Repository
    repo_path: str
    repo_url: str

    nvidia_api_key: str
    nvidia_model: str

    smtp_server: str
    smtp_port: int
    smtp_email: str
    smtp_password: str

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()