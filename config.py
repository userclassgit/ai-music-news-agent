import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# News API Configuration
NEWS_API_KEY = os.getenv('NEWSAPI_KEY')
NEWS_SOURCES = [
    'techcrunch.com',
    'theverge.com',
    'wired.com',
    'engadget.com',
    'billboard.com',
    'pitchfork.com',
    'rollingstone.com'
]
NEWS_KEYWORDS = ['AI', 'artificial intelligence', 'music', 'generative ai']
NEWS_SEARCH_PERIOD = '7d'  # Look for news from the last 7 days

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
AUDIO_FORMAT = 'mp3'
AUDIO_QUALITY = 'high'

# File paths
TEMP_DIR = 'temp'
ASSETS_DIR = 'assets'
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
LOG_FILE = 'bot.log'

# Create necessary directories
for directory in [TEMP_DIR, ASSETS_DIR, AUDIO_DIR]:
    os.makedirs(directory, exist_ok=True)
