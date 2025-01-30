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
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string from RSS feed."""
        try:
            # Remove timezone name (e.g., GMT) and parse
            date_str = ' '.join(date_str.split()[:-1])
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
        except Exception as e:
            self.logger.error(f"Error parsing date: {str(e)}")
            raise
    
    def _extract_article_content(self, url: str) -> str:
        """Extract full article content using trafilatura."""
        try:
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # First, follow any redirects to get the final URL
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            final_url = response.url
            
            # Try trafilatura first
            downloaded = trafilatura.fetch_url(final_url)
            if downloaded:
                content = trafilatura.extract(downloaded)
                if content:
                    return content
            
            # Fallback: Try using requests and BeautifulSoup if trafilatura fails
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find the main article content
            article = soup.find('article')
            if article:
                text = article.get_text(separator='\n\n')
            else:
                # If no article tag, try common content containers
                content_div = soup.find(['div', 'main'], class_=lambda x: x and any(word in str(x).lower() for word in ['content', 'article', 'story', 'body']))
                text = content_div.get_text(separator='\n\n') if content_div else soup.get_text(separator='\n\n')
            
            # Clean up the text
            lines = [line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) > 50]  # Only keep substantial lines
            content = '\n\n'.join(lines)
            
            return content if content else None
            
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
                    pub_date = self._parse_date(entry.published)
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
