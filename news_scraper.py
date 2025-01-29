import feedparser
from datetime import datetime, timedelta
import logging
import requests
from bs4 import BeautifulSoup
import trafilatura

logger = logging.getLogger(__name__)

class NewsArticle:
    def __init__(self, title: str, preview: str, full_content: str = None, source: str = None, 
                 url: str = None, date: datetime = None):
        self.title = title
        self.preview = preview  # First paragraph or snippet
        self.full_content = full_content  # Full article text (only fetched when needed)
        self.source = source
        self.url = url
        self.date = date

class NewsScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Search for articles from last 7 days
        self.feed_url = "https://news.google.com/rss/search?q=AI+music+when:7d&hl=en-US&gl=US&ceid=US:en"
    
    def _contains_keywords(self, text: str) -> bool:
        """Check if text contains both 'AI' and 'music'."""
        text_lower = text.lower()
        return 'ai' in text_lower and 'music' in text_lower
    
    def _extract_article_content(self, url: str) -> str:
        """Extract full article content using trafilatura."""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded)
            return None
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            return None
    
    def get_articles(self):
        """Fetch articles from Google News that have both 'AI' and 'music' in title or preview."""
        try:
            feed = feedparser.parse(self.feed_url)
            articles = []
            
            # Get articles from the last 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for entry in feed.entries:
                try:
                    # Parse date
                    pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                    if pub_date < cutoff_date:
                        continue
                    
                    title = entry.title
                    preview = entry.description  # Usually contains first paragraph
                    
                    # Clean up preview (remove HTML tags)
                    soup = BeautifulSoup(preview, 'html.parser')
                    preview = soup.get_text().strip()
                    
                    # Check if both title and preview contain our keywords
                    if not (self._contains_keywords(title) or self._contains_keywords(preview)):
                        continue
                    
                    article = NewsArticle(
                        title=title,
                        preview=preview,
                        source=entry.source.title if 'source' in entry else 'Unknown',
                        url=entry.link,
                        date=pub_date
                    )
                    articles.append(article)
                    self.logger.info(f"Found article: {title}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing article: {str(e)}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching news: {str(e)}")
            return []
    
    def fetch_full_content(self, article: NewsArticle) -> bool:
        """Fetch the full content of an article when needed."""
        if article.full_content is None and article.url:
            content = self._extract_article_content(article.url)
            if content:
                article.full_content = content
                return True
        return False
