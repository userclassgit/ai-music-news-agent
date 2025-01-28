import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory for temporary files
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
AUDIO_FORMAT = 'mp3'
AUDIO_QUALITY = 'high'

# File paths
ASSETS_DIR = 'assets'
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
LOG_FILE = 'bot.log'

# Create necessary directories
for directory in [ASSETS_DIR, AUDIO_DIR]:
    os.makedirs(directory, exist_ok=True)
