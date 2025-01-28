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
    
    def group_similar_articles(self, articles):
        """Group articles that are about the same story.
        Returns a dictionary where:
        - key: A representative title for the group
        - value: List of related articles
        """
        grouped_articles = {}
        
        for article in articles:
            # Convert title to lowercase for better matching
            title_words = set(word.lower() for word in article.title.split())
            
            matched = False
            for group_key in list(grouped_articles.keys()):
                group_words = set(word.lower() for word in group_key.split())
                # Calculate similarity using word overlap
                similarity = len(title_words & group_words) / len(title_words | group_words)
                
                # If titles are similar enough, add to existing group
                if similarity > 0.5:  # 50% word overlap threshold
                    grouped_articles[group_key].append(article)
                    matched = True
                    break
            
            # If no match found, create new group
            if not matched:
                grouped_articles[article.title] = [article]
        
        return grouped_articles

    def create_summary(self, articles):
        """Create an AI-generated summary from the most recent article.
        Log other related articles as sources but don't include them in summary.
        """
        # Log all sources for reference
        sources = [f"{a.source} ({a.date})" for a in articles]
        logger.info(f"Found {len(articles)} related articles from: {', '.join(sources)}")
        
        # Use the most recent article
        main_article = max(articles, key=lambda a: a.date)
        logger.info(f"Using article from {main_article.source} (published {main_article.date})")
        
        # Create AI summary using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Create a clear, concise summary of the article that will be read aloud. Focus on the key points and maintain a natural, conversational tone. Do not mention sources or dates."},
                    {"role": "user", "content": f"Title: {main_article.title}\n\nContent: {main_article.content}"}
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
            return main_article.title

    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get latest news articles
            articles = self.news_scraper.get_articles()
            logger.info(f"Found {len(articles)} articles")
            
            if not articles:
                logger.info("No new articles found")
                return
            
            # Group similar articles
            grouped_articles = self.group_similar_articles(articles)
            logger.info(f"Grouped into {len(grouped_articles)} unique stories")
            
            # Process each group of articles
            for title, article_group in grouped_articles.items():
                try:
                    logger.info(f"Processing story: {title} ({len(article_group)} articles)")
                    
                    # Create AI-generated summary from most recent article
                    summary = self.create_summary(article_group)
                    
                    # Generate audio file for the summary
                    audio_path = self.audio_generator.process_article(summary)
                    logger.info(f"Audio generated: {audio_path}")
                    
                    # Wait between processing to avoid rate limits
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing story: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")


if __name__ == "__main__":
    bot = AINewsBot()
    bot.run()
