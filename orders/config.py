"""
This module contains the configuration settings for the application.
It uses the pydantic library to define the settings and load them from environment variables.

To override the settings, create a .env file in the root directory of the project and add the settings you want to override.
For example:
DEBUG=True
RELOAD=True
WORKERS=4
PORT=8001
DATABASE_URL=postgresql://user:passwd@host:port/db
OAUTH_TOKEN_SECRET=my_secret
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for the application.
    It uses the pydantic library to define the settings and load them from environment variables.
    """

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"

    title: str = "Demo FastAPI: Orders API"
    description: str = "Demo FastAPI project for the Demo Robot Framework Test Suite"
    version: str = "1.0.0"

    database_url: str = "postgresql://user:passwd@host:port/db"
    debug: bool = False
    reload: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4


load_dotenv()
settings = Settings()

__all__: list[str] = ["settings"]
