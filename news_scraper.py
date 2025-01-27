import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from typing import List, Dict
from config import NEWS_API_KEY, NEWS_SOURCES, NEWS_KEYWORDS, NEWS_SEARCH_PERIOD

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
        
    def _is_relevant(self, title: str, content: str) -> bool:
        """Check if the article is relevant to AI and music."""
        text = (title + " " + content).lower()
        has_ai = any(kw in text for kw in ['ai', 'artificial intelligence', 'generative ai'])
        has_music = 'music' in text
        return has_ai and has_music

    def get_news_api_articles(self) -> List[NewsArticle]:
        """Fetch articles from NewsAPI."""
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'apiKey': NEWS_API_KEY,
                'q': '(AI OR "artificial intelligence") AND music',
                'domains': ','.join(NEWS_SOURCES),
                'language': 'en',
                'sortBy': 'publishedAt',
                'from': (datetime.now() - timedelta(days=7)).isoformat()
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            return [
                NewsArticle(
                    title=article['title'],
                    content=article['content'],
                    source=article['source']['name'],
                    url=article['url'],
                    date=datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                )
                for article in articles
                if self._is_relevant(article['title'], article.get('content', ''))
            ]
        except Exception as e:
            self.logger.error(f"Error fetching from NewsAPI: {str(e)}")
            return []

    def get_rss_articles(self) -> List[NewsArticle]:
        """Fetch articles from RSS feeds."""
        rss_feeds = [
            'https://www.musicbusinessworldwide.com/feed/',
            'https://www.musictech.net/feed/',
            'https://www.billboard.com/feed/'
        ]
        
        articles = []
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    if hasattr(entry, 'published_parsed'):
                        date = datetime(*entry.published_parsed[:6])
                    else:
                        date = datetime.now()
                    
                    if date < datetime.now() - timedelta(days=7):
                        continue
                        
                    if self._is_relevant(entry.title, entry.description):
                        articles.append(NewsArticle(
                            title=entry.title,
                            content=entry.description,
                            source=feed.feed.title,
                            url=entry.link,
                            date=date
                        ))
            except Exception as e:
                self.logger.error(f"Error fetching RSS feed {feed_url}: {str(e)}")
                
        return articles

    def get_articles(self) -> List[NewsArticle]:
        """Get articles from all sources and remove duplicates."""
        all_articles = []
        all_articles.extend(self.get_news_api_articles())
        all_articles.extend(self.get_rss_articles())
        
        # Remove duplicates based on title similarity
        unique_articles = []
        seen_titles = set()
        
        for article in all_articles:
            title_key = article.title.lower()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        return sorted(unique_articles, key=lambda x: x.date, reverse=True)
