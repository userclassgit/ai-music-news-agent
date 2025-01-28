import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory configuration
ASSETS_DIR = 'assets'
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')

# Create necessary directories
os.makedirs(AUDIO_DIR, exist_ok=True)

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
AUDIO_FORMAT = 'mp3'
AUDIO_QUALITY = 'high'

# File paths
LOG_FILE = 'bot.log'

# Create necessary directories
os.makedirs(ASSETS_DIR, exist_ok=True)
