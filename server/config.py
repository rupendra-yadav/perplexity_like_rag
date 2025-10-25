from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TAVILY_API_KEY:str = "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"