import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/vocabulary.db")

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
