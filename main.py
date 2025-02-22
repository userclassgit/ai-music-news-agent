import os
import logging
from datetime import datetime, timedelta
import google.generativeai as genai
from newsapi import NewsApiClient
from audio_generator import AudioGenerator
from config import AUDIO_DIR, GEMINI_API_KEY, NEWS_API_KEY
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
    
    def scrape_article_content(self, url):
        """Scrape article content from URL."""
        try:
            # Don't scrape certain domains that block scraping
            domain = urlparse(url).netloc
            if any(blocked in domain for blocked in ['bloomberg.com', 'ft.com', 'wsj.com']):
                return None

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Basic cleaning
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            
            return text[:5000]  # Limit content length
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

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
                sort_by='publishedAt'
            )
            
            if not articles['articles']:
                logger.info("No articles found in the past 2 days")
                return "No news about AI and music found in the past 2 days."
            
            # Format articles with content for Gemini
            formatted_articles = []
            for article in articles['articles']:
                logger.info(f"Scraping content from: {article['url']}")
                content = self.scrape_article_content(article['url'])
                if content:
                    formatted_articles.append(
                        f"Title: {article['title']}\n" 
                        f"Date: {article['publishedAt']}\n" 
                        f"Content:\n{content}\n"
                    )
            
            if not formatted_articles:
                return "Could not retrieve content from any articles."
            
            articles_text = "\n---\n".join(formatted_articles)
            
            # Send to Gemini for summarization
            logger.info("Sending articles to Gemini for summarization...")
            query = f"""
Summarize the following articles about AI and music news. Important requirements:

1. Only summarize articles that discuss BOTH AI and music - skip others
2. Professional tone - no YouTube-style enthusiasm
3. No source attribution (don't say "According to...") 
4. No meta-references (don't say "This article...")
5. One concise paragraph per relevant article
6. Begin each summary directly with the news
7. Skip any examples - analyze ONLY the articles provided below

Articles to analyze:

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
        """Test the complete news summary workflow."""
        try:
            logger.info("Testing complete workflow...")
            
            # First show raw NewsAPI results
            end_date = datetime.now()
            start_date = end_date - timedelta(days=2)
            
            articles = self.newsapi.get_everything(
                q='AI music',
                from_param=start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='publishedAt'
            )
            
            print("\nStep 1. Raw NewsAPI articles:\n")
            for article in articles['articles']:
                print(f"Title: {article['title']}")
                print(f"Date: {article['publishedAt']}")
                print(f"URL: {article['url']}")
                print("---")
            
            print("\nStep 2. Getting Gemini summary...\n")
            summary = self.get_news_summary()
            if summary:
                print(summary)
                print("\nWorkflow completed successfully!")
            else:
                logger.error("Failed to generate summary")
            
        except Exception as e:
            logger.error(f"Error in test_prompt: {str(e)}")

if __name__ == "__main__":
    bot = AINewsBot()
    # For testing, use test_prompt() instead of run()
    bot.test_prompt()
