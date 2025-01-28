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
        """Create a comprehensive summary from multiple articles about the same story.
        Includes attribution to original sources.
        """
        # Extract key information
        main_article = articles[0]  # Use first article as primary source
        sources = [f"{a.source} ({a.published_date})" for a in articles]
        
        # Create summary
        summary = f"# {main_article.title}\n\n"
        summary += f"Based on {len(articles)} sources: {', '.join(sources)}\n\n"
        
        # Add content from all articles, avoiding repetition
        unique_paragraphs = set()
        for article in articles:
            for paragraph in article.content.split('\n'):
                # Only add unique paragraphs
                if paragraph.strip() and paragraph not in unique_paragraphs:
                    unique_paragraphs.add(paragraph)
        
        summary += "\n".join(unique_paragraphs)
        return summary

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
                    
                    # Create a summary of all related articles
                    summary = self.create_summary(article_group)
                    
                    # Generate single audio file for the summary
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
