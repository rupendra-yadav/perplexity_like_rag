from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

# Load variables from .env file
load_dotenv()

class Settings(BaseSettings):
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

