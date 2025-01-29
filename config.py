import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory for audio files
AUDIO_DIR = "/Users/bruh/Desktop/AI news audio files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Logging
LOG_FILE = "bot.log"
