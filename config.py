import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory for audio files
AUDIO_DIR = "/Users/bruh/Desktop/AI music news audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Logging
LOG_FILE = "bot.log"
