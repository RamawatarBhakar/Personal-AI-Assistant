import os
from dotenv import load_dotenv

# .env file ko load karo
load_dotenv()

# Variables fetch karo
API_ID = int(os.getenv("API_ID", 6))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
JINA_API_KEY = os.getenv("JINA_API_KEY", "")

# Validation (Agar jaruri keys missing hongi toh script pehle hi bata degi)
if not BOT_TOKEN or not GROQ_API_KEY:
    print("⚠️ WARNING: BOT_TOKEN ya GROQ_API_KEY missing hai .env file me!")