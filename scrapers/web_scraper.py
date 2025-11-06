"""
Web Scraper using NewsAPI for NDTA News Pipeline
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict

log = logging.getLogger(__name__)


class WebScraper:
    """Scrapes news using NewsAPI"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config['env'].get('newsapi_key')
        self.base_url = "https://newsapi.org/v2/everything"
    
    def search_news(self, keywords: List[str], lookback_days: int = 7) -> List[Dict]:
        """Search for news using keywords"""
        
        if not self.api_key:
            log.warning("NewsAPI key not configured, skipping web scraping")
            return []
        
        articles = []
        
        # Build query from keywords
        query = ' OR '.join([f'"{kw}"' for kw in keywords[:5]])  # Limit to 5 keywords
        
        # Calculate date range
        from_date = (datetime.now() - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': from_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': self.api_key,
            'pageSize': 100,
        }
        
        try:
            log.info(f"Searching NewsAPI with query: {query}")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'ok':
                for item in data.get('articles', []):
                    article = {
                        'id': item.get('url', ''),
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'description': item.get('description', ''),
                        'summary': item.get('description', ''),
                        'content': item.get('content', ''),
                        'published_date': item.get('publishedAt', ''),
                        'source': item.get('source', {}).get('name', 'Unknown'),
                        'source_type': 'newsapi',
                        'category': 'Industry News',
                        'is_relevant': True,  # NewsAPI results are pre-filtered
                        'relevance_score': 7.0,  # Default score for NewsAPI articles
                        'is_state_specific': False,
                        'status': 'pending_review',
                        'scraped_at': datetime.now().isoformat(),
                    }
                    articles.append(article)
                
                log.info(f"Found {len(articles)} articles from NewsAPI")
            else:
                log.error(f"NewsAPI error: {data.get('message')}")
        
        except Exception as e:
            log.error(f"Error searching NewsAPI: {e}")
        
        return articles
    
    def scrape_all(self, lookback_days: int = 7) -> List[Dict]:
        """Scrape news from all configured sources"""
        
        # Get keywords from config
        primary_keywords = self.config.get('primary_keywords', [])
        
        if not primary_keywords:
            log.warning("No keywords configured")
            return []
        
        return self.search_news(primary_keywords, lookback_days)

