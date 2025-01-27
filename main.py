import os
import logging
import time
from datetime import datetime
from news_scraper import NewsScraper
from audio_generator import AudioGenerator
from config import TEMP_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AINewsBot:
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.audio_generator = AudioGenerator()
        
    def clean_temp_files(self):
        """Clean up temporary files."""
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {str(e)}")

    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get latest news articles
            articles = self.news_scraper.get_articles()
            logger.info(f"Found {len(articles)} relevant articles")
            
            if not articles:
                logger.info("No new articles found")
                return
            
            # Process each article
            for article in articles:
                try:
                    logger.info(f"Processing article: {article.title}")
                    
                    # Generate audio
                    audio_path = self.audio_generator.process_article(article)
                    logger.info(f"Audio generated successfully: {audio_path}")
                    
                    # Wait between processing to avoid rate limits
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")
        
        finally:
            self.clean_temp_files()

if __name__ == "__main__":
    bot = AINewsBot()
    bot.run()
