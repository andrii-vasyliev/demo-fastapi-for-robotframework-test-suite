from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:passwd@host:port/db"
    debug: bool = True
    reload: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    project_name: str = "Demo FastAPI project"
    oauth_token_secret: str = "my_secret"


load_dotenv()
settings = Settings()
