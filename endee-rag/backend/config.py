import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ENDEE_BASE_URL = os.getenv("ENDEE_BASE_URL")