import os
import logging
import time
from datetime import datetime
import openai
import json
from news_scraper import NewsScraper
from audio_generator import AudioGenerator
from config import AUDIO_DIR, OPENAI_API_KEY

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
    
    def categorize_articles(self, articles):
        """Group articles into topics using LLM to analyze titles and previews only."""
        if not articles:
            return {}
        
        # Prepare articles data for LLM
        articles_data = [
            {
                "id": i,
                "title": article.title,
                "preview": article.preview
            }
            for i, article in enumerate(articles)
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a news categorizer. Group articles into topics based on their titles and previews.
                    Return a JSON object where:
                    - Keys are topic identifiers (e.g., "topic_1")
                    - Values are lists of article IDs that belong to that topic
                    Example: {"topic_1": [0, 3, 5], "topic_2": [1, 4], "topic_3": [2]}"""},
                    {"role": "user", "content": f"Categorize these articles:\n{json.dumps(articles_data, indent=2)}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse the response into a dictionary
            categorization = json.loads(response.choices[0].message.content)
            
            # Convert the categorization into groups of actual articles
            article_groups = {}
            for topic, article_ids in categorization.items():
                article_groups[topic] = [articles[i] for i in article_ids]
            
            return article_groups
            
        except Exception as e:
            logger.error(f"Error categorizing articles: {str(e)}")
            # Fallback: treat each article as its own topic
            return {f"topic_{i}": [article] for i, article in enumerate(articles)}
    
    def select_representative_article(self, articles):
        """Select the most suitable article from a group to summarize."""
        # For now, use the most recent article
        return max(articles, key=lambda a: a.date)
    
    def create_summary(self, article):
        """Create an AI-generated summary from the article."""
        try:
            # Fetch full content if not already available
            if not article.full_content:
                if not self.news_scraper.fetch_full_content(article):
                    logger.error(f"Could not fetch full content for article: {article.title}")
                    return None
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Create a clear, concise summary of the article that will be read aloud. Focus on the key points and maintain a natural, conversational tone. Do not mention sources."},
                    {"role": "user", "content": f"Title: {article.title}\n\nContent: {article.full_content}"}
                ],
                temperature=0.7,
                max_tokens=250  # Limit summary length to control costs
            )
            summary = response.choices[0].message.content.strip()
            logger.info("Successfully generated AI summary")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {str(e)}")
            return None

    def run(self):
        """Main bot execution loop."""
        try:
            logger.info("Starting AI News Bot")
            
            # Get latest news articles
            articles = self.news_scraper.get_articles()
            logger.info(f"Found {len(articles)} AI music articles")
            
            if not articles:
                logger.info("No new articles found")
                return
            
            # Group articles by topic
            article_groups = self.categorize_articles(articles)
            logger.info(f"Grouped into {len(article_groups)} topics")
            
            # Process each topic
            for topic_id, group in article_groups.items():
                try:
                    logger.info(f"Processing topic {topic_id} with {len(group)} articles")
                    
                    # Log all articles in this topic
                    for article in group:
                        logger.info(f"- {article.title} ({article.source}, {article.date})")
                    
                    # Select one article to summarize
                    main_article = self.select_representative_article(group)
                    logger.info(f"Selected article for summary: {main_article.title}")
                    
                    # Create AI-generated summary
                    summary = self.create_summary(main_article)
                    if not summary:
                        logger.error("Failed to create summary, skipping topic")
                        continue
                    
                    # Generate audio file
                    audio_path = self.audio_generator.process_article(summary)
                    logger.info(f"Audio generated: {audio_path}")
                    
                    # Wait between processing to avoid rate limits
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing topic: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Bot execution error: {str(e)}")


if __name__ == "__main__":
    bot = AINewsBot()
    bot.run()
