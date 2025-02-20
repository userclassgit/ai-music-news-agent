import os
import logging
from datetime import datetime, timedelta
import google.generativeai as genai
from audio_generator import AudioGenerator
from config import AUDIO_DIR, GEMINI_API_KEY

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
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
        self.audio_generator = AudioGenerator()
    
    def get_news_summary(self):
        """Get AI music news summary using Gemini API."""
        current_date = datetime.now().strftime('%B %d, %Y')
        query = f"""
          Today's date is {current_date}. What's the date 7 days ago?
        """
        
        try:
            response = self.model.generate_content(query)
            logger.info("Successfully generated news summary using Gemini API")
            return response.text
        except Exception as e:
            logger.error(f"Error getting news summary: {str(e)}")
            return None
 
    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get news summary from Sonar
            summary = self.get_news_summary()
            if not summary:
                logger.info("No news summary generated")
                return
            
            # Generate audio file
            audio_path = self.audio_generator.process_article(summary)
            logger.info(f"Audio generated: {audio_path}")
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")


    def test_prompt(self):
        """Test the Gemini prompt without audio conversion."""
        try:
            logger.info("Testing Gemini prompt...")
            summary = self.get_news_summary()
            if summary:
                print("\nGemini Response:\n")
                print(summary)
            else:
                print("No summary generated")
        except Exception as e:
            logger.error(f"Error in test: {str(e)}")

if __name__ == "__main__":
    bot = AINewsBot()
    # For testing, use test_prompt() instead of run()
    bot.test_prompt()
