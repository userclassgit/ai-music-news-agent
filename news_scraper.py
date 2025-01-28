import feedparser
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NewsArticle:
    def __init__(self, title: str, content: str, source: str, url: str, date: datetime):
        self.title = title
        self.content = content
        self.source = source
        self.url = url
        self.date = date

class NewsScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.feed_url = "https://news.google.com/rss/search?q=AI+music&hl=en-US&gl=US&ceid=US:en"
    
    def _contains_keywords(self, title: str) -> bool:
        """Check if title contains both 'AI' and 'music'."""
        title_lower = title.lower()
        return 'ai' in title_lower and 'music' in title_lower
    
    def get_articles(self):
        """Fetch articles from Google News that have both 'AI' and 'music' in title."""
        try:
            feed = feedparser.parse(self.feed_url)
            
            # Dictionary to track seen titles to avoid duplicates
            seen_titles = set()
            articles = []
            
            for entry in feed.entries:
                title = entry.title
                
                # Skip if we've seen a similar title or if it doesn't contain both keywords
                if not self._contains_keywords(title):
                    continue
                    
                # Skip if we've seen this title or a similar one
                title_words = set(title.lower().split())
                for seen_title in seen_titles:
                    seen_words = set(seen_title.lower().split())
                    # If titles share more than 50% words, consider it a duplicate
                    if len(title_words & seen_words) / len(title_words | seen_words) > 0.5:
                        self.logger.info(f"Skipping similar article: {title}")
                        continue
                
                # Add this title to seen titles
                seen_titles.add(title)
                
                try:
                    article = NewsArticle(
                        title=title,
                        content=entry.description,  # RSS feed usually includes article summary
                        source=entry.source.title if 'source' in entry else 'Unknown',
                        url=entry.link,
                        date=datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                    )
                    articles.append(article)
                    self.logger.info(f"Found article: {title}")
                except Exception as e:
                    self.logger.error(f"Error processing article {title}: {str(e)}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching news: {str(e)}")
            return []
