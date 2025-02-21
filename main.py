import os
import logging
from datetime import datetime, timedelta
import google.generativeai as genai
from newsapi import NewsApiClient
from audio_generator import AudioGenerator
from config import AUDIO_DIR, GEMINI_API_KEY, NEWS_API_KEY

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
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        self.audio_generator = AudioGenerator()
    
    def get_news_summary(self):
        """Get AI music news summary using NewsAPI and Gemini."""
        try:
            # Calculate dates for the past 2 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=2)
            
            # Get news articles from NewsAPI
            logger.info("Fetching news from NewsAPI...")
            articles = self.newsapi.get_everything(
                q='AI music',
                from_param=start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='publishedAt',
                page_size=100
            )
            
            if not articles['articles']:
                logger.info("No articles found in the past 2 days")
                return "No news about AI and music found in the past 2 days."
            
            # Format articles for Gemini
            articles_text = "\n\n".join(
                f"Title: {article['title']}\n" 
                f"Date: {article['publishedAt']}\n" 
                f"Description: {article['description']}\n" 
                f"URL: {article['url']}"
                for article in articles['articles']
            )
            
            # Send to Gemini for summarization
            logger.info("Sending articles to Gemini for summarization...")
            query = f"""
            You are a professional news anchor specializing in AI and music news. Here are news articles from the past 2 days.
            Please create a natural, engaging summary following these guidelines:

            1. Only summarize articles that discuss BOTH AI and music technology (not just one topic)
            2. Skip duplicate news events - if multiple articles cover the same story, only summarize it once
            3. Present each summary in a conversational style as if speaking to a YouTube audience
            4. Include the exact publishing date in mm-dd-yyyy format for each summary
            5. If no articles discuss both AI and music, simply state that there's no relevant news
            6. Focus on factual reporting while maintaining an engaging tone

            Here are the articles to analyze:

            {articles_text}
            """
            
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
            
            # Get news summary
            summary = self.get_news_summary()
            if not summary:
                logger.error("Failed to get news summary")
                return
            
            logger.info("Successfully got news summary")
            
            # Generate audio from summary
            audio_file = self.audio_generator.generate_audio(summary)
            if not audio_file:
                logger.error("Failed to generate audio")
                return
            
            logger.info(f"Successfully generated audio file: {audio_file}")
            
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")

    def test_prompt(self):
        """Test the news summary generation without audio."""
        try:
            logger.info("Testing news summary generation...")
            summary = self.get_news_summary()
            if summary:
                print("\nGenerated Summary:\n")
                print(summary)
                print("\nTest completed successfully!")
            else:
                logger.error("Failed to generate summary")
        except Exception as e:
            logger.error(f"Error in test_prompt: {str(e)}")

if __name__ == "__main__":
    bot = AINewsBot()
    # For testing, use test_prompt() instead of run()
    bot.test_prompt()
