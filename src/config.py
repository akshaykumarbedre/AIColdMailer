import os
from dataclasses import dataclass
from dotenv import load_dotenv
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logging/cold_email_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@dataclass
class Config:
    GROQ_API_KEY: str
    LANGCHAIN_API_KEY: str
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_PROJECT: str = "cold email automation"

    @classmethod
    def load_from_env(cls):
        load_dotenv()
        return cls(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY", ""),
            SENDER_EMAIL=os.getenv("SENDER_EMAIL", ""),
            SENDER_PASSWORD=os.getenv("SENDER_PASSWORD", "")
        )