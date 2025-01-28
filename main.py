import os
import logging
import time
from datetime import datetime
import openai
from news_scraper import NewsScraper
from audio_generator import AudioGenerator
from config import TEMP_DIR, OPENAI_API_KEY

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
        openai.api_key = OPENAI_API_KEY
    
    def create_summary(self, article):
        """Create an AI-generated summary from the article."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Create a clear, concise summary of the article that will be read aloud. Focus on the key points and maintain a natural, conversational tone. Do not mention sources or dates."},
                    {"role": "user", "content": f"Title: {article.title}\n\nContent: {article.content}"}
                ],
                temperature=0.7,
                max_tokens=250  # Limit summary length to control costs
            )
            summary = response.choices[0].message.content.strip()
            logger.info("Successfully generated AI summary")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {str(e)}")
            # Fallback to using the article title if AI summarization fails
            return article.title

    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get latest news articles
            articles = self.news_scraper.get_articles()
            logger.info(f"Found {len(articles)} unique AI music articles")
            
            if not articles:
                logger.info("No new articles found")
                return
            
            # Process each unique article
            for article in articles:
                try:
                    logger.info(f"Processing article: {article.title}")
                    logger.info(f"Source: {article.source} (published {article.date})")
                    
                    # Create AI-generated summary
                    summary = self.create_summary(article)
                    
                    # Generate audio file
                    audio_path = self.audio_generator.process_article(summary)
                    logger.info(f"Audio generated: {audio_path}")
                    
                    # Wait between processing to avoid rate limits
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")


if __name__ == "__main__":
    bot = AINewsBot()
    bot.run()
