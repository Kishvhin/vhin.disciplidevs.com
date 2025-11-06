"""
RSS Feed Scraper for NDTA News Pipeline
"""
import feedparser
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import time

log = logging.getLogger(__name__)


class RSSFeedScraper:
    """Scrapes RSS feeds for news articles"""
    
    def __init__(self, config):
        self.config = config
        self.feeds = config.get('rss_feeds', [])
    
    def scrape_feed(self, feed_url: str, feed_name: str, lookback_days: int = 7) -> List[Dict]:
        """Scrape a single RSS feed"""
        articles = []
        
        try:
            log.info(f"Scraping RSS feed: {feed_name}")
            feed = feedparser.parse(feed_url)
            
            cutoff_date = datetime.now() - timedelta(days=lookback_days)
            
            for entry in feed.entries:
                try:
                    # Parse published date
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        pub_date = datetime(*entry.updated_parsed[:6])
                    else:
                        pub_date = datetime.now()
                    
                    # Skip old articles
                    if pub_date < cutoff_date:
                        continue
                    
                    article = {
                        'id': entry.get('id', entry.get('link', '')),
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'description': entry.get('summary', entry.get('description', '')),
                        'summary': entry.get('summary', entry.get('description', '')),
                        'published_date': pub_date.isoformat(),
                        'source': feed_name,
                        'source_type': 'rss',
                        'category': 'Industry News',
                        'is_relevant': True,  # RSS feeds are pre-filtered
                        'relevance_score': 7.0,  # Default score for RSS articles
                        'is_state_specific': False,
                        'status': 'pending_review',
                        'scraped_at': datetime.now().isoformat(),
                    }
                    
                    articles.append(article)
                    
                except Exception as e:
                    log.warning(f"Error parsing entry from {feed_name}: {e}")
                    continue
            
            log.info(f"Found {len(articles)} articles from {feed_name}")
            
        except Exception as e:
            log.error(f"Error scraping feed {feed_name}: {e}")
        
        return articles
    
    def scrape_all_feeds(self, lookback_days: int = 7) -> List[Dict]:
        """Scrape all configured RSS feeds"""
        all_articles = []
        
        for feed in self.feeds:
            feed_url = feed.get('url')
            feed_name = feed.get('name')
            
            if not feed_url or not feed_name:
                continue
            
            articles = self.scrape_feed(feed_url, feed_name, lookback_days)
            all_articles.extend(articles)
            
            # Rate limiting
            time.sleep(2)
        
        log.info(f"Total articles from RSS feeds: {len(all_articles)}")
        return all_articles

