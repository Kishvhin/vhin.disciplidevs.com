"""
Reddit Scraper for NDTA News Pipeline
Scrapes dump truck conversations from relevant subreddits
"""
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import time

log = logging.getLogger(__name__)


class RedditScraper:
    """Scrape dump truck discussions from Reddit"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.reddit_config = config.get('reddit', {})
        self.base_url = "https://www.reddit.com"
        
        # Subreddits to monitor
        self.subreddits = self.reddit_config.get('subreddits', [
            'Truckers',
            'trucking',
            'Construction',
            'heavyequipment',
            'CommercialTrucking',
            'OwnerOperators',
            'Diesel',
            'mechanics'
        ])
        
        # Keywords to search for
        self.keywords = self.reddit_config.get('keywords', [
            'dump truck',
            'dump trailer',
            'tipper truck',
            'aggregate hauling',
            'material hauling'
        ])
    
    def scrape_subreddit(self, subreddit: str, lookback_days: int = 7) -> List[Dict]:
        """Scrape posts from a specific subreddit"""
        posts = []
        
        try:
            # Use Reddit's JSON API (no auth required for public posts)
            url = f"{self.base_url}/r/{subreddit}/new.json"
            headers = {
                'User-Agent': 'NDTA News Pipeline Bot 1.0'
            }
            
            params = {
                'limit': 100  # Max posts per request
            }
            
            log.info(f"Scraping r/{subreddit}...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                cutoff_date = datetime.now() - timedelta(days=lookback_days)
                
                for post_data in data.get('data', {}).get('children', []):
                    post = post_data.get('data', {})
                    
                    # Check if post is recent enough
                    post_time = datetime.fromtimestamp(post.get('created_utc', 0))
                    if post_time < cutoff_date:
                        continue
                    
                    # Check if post contains relevant keywords
                    title = post.get('title', '').lower()
                    selftext = post.get('selftext', '').lower()
                    combined_text = f"{title} {selftext}"
                    
                    is_relevant = any(keyword.lower() in combined_text for keyword in self.keywords)
                    
                    if is_relevant:
                        article = {
                            'title': post.get('title', ''),
                            'description': post.get('selftext', '')[:500] or post.get('title', ''),
                            'url': f"{self.base_url}{post.get('permalink', '')}",
                            'source': f"Reddit - r/{subreddit}",
                            'published_date': post_time.isoformat(),
                            'author': post.get('author', 'unknown'),
                            'score': post.get('score', 0),
                            'num_comments': post.get('num_comments', 0),
                            'subreddit': subreddit,
                            'post_type': 'reddit_discussion',
                            'scraped_at': datetime.now().isoformat()
                        }
                        posts.append(article)
                        log.info(f"  ✓ Found relevant post: {article['title'][:60]}...")
            
            else:
                log.warning(f"Failed to scrape r/{subreddit}: HTTP {response.status_code}")
            
            # Rate limiting - be nice to Reddit
            time.sleep(2)
            
        except Exception as e:
            log.error(f"Error scraping r/{subreddit}: {e}")
        
        return posts
    
    def search_reddit(self, query: str, lookback_days: int = 7) -> List[Dict]:
        """Search Reddit for specific keywords"""
        posts = []
        
        try:
            url = f"{self.base_url}/search.json"
            headers = {
                'User-Agent': 'NDTA News Pipeline Bot 1.0'
            }
            
            params = {
                'q': query,
                'sort': 'new',
                'limit': 100,
                't': 'week' if lookback_days <= 7 else 'month'
            }
            
            log.info(f"Searching Reddit for: {query}")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                cutoff_date = datetime.now() - timedelta(days=lookback_days)
                
                for post_data in data.get('data', {}).get('children', []):
                    post = post_data.get('data', {})
                    
                    post_time = datetime.fromtimestamp(post.get('created_utc', 0))
                    if post_time < cutoff_date:
                        continue
                    
                    article = {
                        'title': post.get('title', ''),
                        'description': post.get('selftext', '')[:500] or post.get('title', ''),
                        'url': f"{self.base_url}{post.get('permalink', '')}",
                        'source': f"Reddit - r/{post.get('subreddit', 'unknown')}",
                        'published_date': post_time.isoformat(),
                        'author': post.get('author', 'unknown'),
                        'score': post.get('score', 0),
                        'num_comments': post.get('num_comments', 0),
                        'subreddit': post.get('subreddit', 'unknown'),
                        'post_type': 'reddit_discussion',
                        'search_query': query,
                        'scraped_at': datetime.now().isoformat()
                    }
                    posts.append(article)
                    log.info(f"  ✓ Found: {article['title'][:60]}...")
            
            else:
                log.warning(f"Failed to search Reddit: HTTP {response.status_code}")
            
            time.sleep(2)
            
        except Exception as e:
            log.error(f"Error searching Reddit: {e}")
        
        return posts
    
    def scrape_all(self, lookback_days: int = 7) -> List[Dict]:
        """Scrape all configured subreddits and searches"""
        all_posts = []
        
        log.info(f"Starting Reddit scrape (lookback: {lookback_days} days)")
        
        # Scrape each subreddit
        for subreddit in self.subreddits:
            posts = self.scrape_subreddit(subreddit, lookback_days)
            all_posts.extend(posts)
        
        # Search for specific keywords
        for keyword in self.keywords:
            posts = self.search_reddit(keyword, lookback_days)
            all_posts.extend(posts)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_posts = []
        for post in all_posts:
            if post['url'] not in seen_urls:
                seen_urls.add(post['url'])
                unique_posts.append(post)
        
        log.info(f"Reddit scrape complete: {len(unique_posts)} unique posts found")
        
        return unique_posts

