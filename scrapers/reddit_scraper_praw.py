"""
Reddit Scraper using PRAW (Official Reddit API)
Improved version with OAuth authentication and higher rate limits
"""

import praw
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

log = logging.getLogger(__name__)


class RedditScraperPRAW:
    """
    Reddit scraper using PRAW (Python Reddit API Wrapper)
    
    Benefits over basic scraper:
    - 10x higher rate limits (600 requests per 10 minutes)
    - Official API support
    - More reliable
    - Access to more data
    - Can post to Reddit (if needed)
    """
    
    def __init__(self, config: dict):
        """Initialize Reddit scraper with PRAW"""
        self.config = config
        
        # Get Reddit credentials from environment
        env_config = config.get('env', {})
        client_id = env_config.get('reddit_client_id')
        client_secret = env_config.get('reddit_client_secret')
        user_agent = env_config.get('reddit_user_agent', 'NDTA News Pipeline v1.0')
        username = env_config.get('reddit_username')
        password = env_config.get('reddit_password')
        
        # Initialize PRAW Reddit instance in read-only mode
        # Read-only mode is perfect for scraping - no password needed!
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )

            # Set to read-only mode
            self.reddit.read_only = True

            log.info(f"✅ Reddit API connected (read-only mode)")
            log.info(f"   Rate limit: 600 requests per 10 minutes")

        except Exception as e:
            log.error(f"❌ Failed to connect to Reddit API: {e}")
            raise
        
        # Get configuration
        reddit_config = config.get('reddit', {})
        self.subreddits = reddit_config.get('subreddits', ['Truckers', 'trucking'])
        self.keywords = reddit_config.get('keywords', ['dump truck'])
        self.min_score = reddit_config.get('min_score', 5)
        self.min_comments = reddit_config.get('min_comments', 2)
    
    def scrape_subreddit(self, subreddit_name: str, lookback_days: int = 7) -> List[Dict]:
        """
        Scrape posts from a specific subreddit
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            lookback_days: How many days back to look
            
        Returns:
            List of post dictionaries
        """
        posts = []
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get new posts (last 100)
            for submission in subreddit.new(limit=100):
                # Check if post is within lookback period
                post_date = datetime.fromtimestamp(submission.created_utc)
                if post_date < cutoff_date:
                    continue
                
                # Check if post meets quality thresholds
                if submission.score < self.min_score:
                    continue
                if submission.num_comments < self.min_comments:
                    continue
                
                # Check if post is relevant (contains keywords)
                text = f"{submission.title} {submission.selftext}".lower()
                if not any(keyword.lower() in text for keyword in self.keywords):
                    continue
                
                # Extract post data
                # Calculate relevance score based on engagement
                relevance_score = min(10, 5 + (submission.score / 100) + (submission.num_comments / 10))

                post = {
                    'id': submission.id,
                    'title': submission.title,
                    'description': submission.selftext[:500] if submission.selftext else submission.title,
                    'url': f"https://reddit.com{submission.permalink}",
                    'source': f"Reddit - r/{subreddit_name}",
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'subreddit': subreddit_name,
                    'published_date': post_date.isoformat(),
                    'category': 'Reddit Discussion',
                    'upvote_ratio': submission.upvote_ratio,
                    'is_self': submission.is_self,
                    'link_flair_text': submission.link_flair_text or '',
                    'is_relevant': True,  # Already filtered by keywords
                    'relevance_score': round(relevance_score, 1),
                    'is_state_specific': False,  # Reddit posts are not state-specific
                    'status': 'pending_review',
                    'scraped_at': datetime.now().isoformat(),
                }
                
                posts.append(post)
            
            log.info(f"✅ r/{subreddit_name}: Found {len(posts)} relevant posts")
            
        except Exception as e:
            log.error(f"❌ Error scraping r/{subreddit_name}: {e}")
        
        return posts
    
    def search_reddit(self, query: str, lookback_days: int = 7, limit: int = 100) -> List[Dict]:
        """
        Search all of Reddit for specific keywords
        
        Args:
            query: Search query
            lookback_days: How many days back to look
            limit: Maximum number of results
            
        Returns:
            List of post dictionaries
        """
        posts = []
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        
        try:
            # Search all of Reddit
            for submission in self.reddit.subreddit('all').search(query, limit=limit, sort='new'):
                # Check if post is within lookback period
                post_date = datetime.fromtimestamp(submission.created_utc)
                if post_date < cutoff_date:
                    continue
                
                # Check if post meets quality thresholds
                if submission.score < self.min_score:
                    continue
                if submission.num_comments < self.min_comments:
                    continue
                
                # Extract post data
                # Calculate relevance score based on engagement
                relevance_score = min(10, 5 + (submission.score / 100) + (submission.num_comments / 10))

                post = {
                    'id': submission.id,
                    'title': submission.title,
                    'description': submission.selftext[:500] if submission.selftext else submission.title,
                    'url': f"https://reddit.com{submission.permalink}",
                    'source': f"Reddit - r/{submission.subreddit.display_name}",
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'subreddit': submission.subreddit.display_name,
                    'published_date': post_date.isoformat(),
                    'category': 'Reddit Discussion',
                    'upvote_ratio': submission.upvote_ratio,
                    'is_self': submission.is_self,
                    'link_flair_text': submission.link_flair_text or '',
                    'is_relevant': True,  # Already filtered by keywords
                    'relevance_score': round(relevance_score, 1),
                    'is_state_specific': False,  # Reddit posts are not state-specific
                    'status': 'pending_review',
                    'scraped_at': datetime.now().isoformat(),
                }
                
                posts.append(post)
            
            log.info(f"✅ Reddit search '{query}': Found {len(posts)} posts")
            
        except Exception as e:
            log.error(f"❌ Error searching Reddit for '{query}': {e}")
        
        return posts
    
    def scrape_all(self, lookback_days: int = 7) -> List[Dict]:
        """
        Scrape all configured subreddits and search queries
        
        Args:
            lookback_days: How many days back to look
            
        Returns:
            List of unique post dictionaries
        """
        all_posts = []
        seen_urls = set()
        
        log.info(f"🔍 Starting Reddit scrape with PRAW (lookback: {lookback_days} days)")
        
        # Scrape configured subreddits
        for subreddit in self.subreddits:
            posts = self.scrape_subreddit(subreddit, lookback_days)
            
            # Add unique posts
            for post in posts:
                if post['url'] not in seen_urls:
                    all_posts.append(post)
                    seen_urls.add(post['url'])
            
            # Rate limiting (be nice to Reddit)
            time.sleep(2)
        
        # Search for keywords
        for keyword in self.keywords:
            posts = self.search_reddit(keyword, lookback_days, limit=50)
            
            # Add unique posts
            for post in posts:
                if post['url'] not in seen_urls:
                    all_posts.append(post)
                    seen_urls.add(post['url'])
            
            # Rate limiting
            time.sleep(2)
        
        log.info(f"✅ Reddit scrape complete: {len(all_posts)} unique posts")
        
        return all_posts
    
    def post_to_reddit(self, subreddit_name: str, title: str, content: str, 
                       is_self_post: bool = True) -> Optional[str]:
        """
        Post content to a subreddit (requires authentication)
        
        Args:
            subreddit_name: Subreddit to post to (without r/)
            title: Post title
            content: Post content (for self posts) or URL (for link posts)
            is_self_post: True for text post, False for link post
            
        Returns:
            URL of created post, or None if failed
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            if is_self_post:
                submission = subreddit.submit(title=title, selftext=content)
            else:
                submission = subreddit.submit(title=title, url=content)
            
            post_url = f"https://reddit.com{submission.permalink}"
            log.info(f"✅ Posted to r/{subreddit_name}: {post_url}")
            
            return post_url
            
        except Exception as e:
            log.error(f"❌ Failed to post to r/{subreddit_name}: {e}")
            return None
    
    def get_hot_posts(self, subreddit_name: str, limit: int = 25) -> List[Dict]:
        """
        Get hot/trending posts from a subreddit
        
        Args:
            subreddit_name: Subreddit name
            limit: Number of posts to get
            
        Returns:
            List of post dictionaries
        """
        posts = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for submission in subreddit.hot(limit=limit):
                # Calculate relevance score based on engagement
                relevance_score = min(10, 5 + (submission.score / 100) + (submission.num_comments / 10))

                post = {
                    'id': submission.id,
                    'title': submission.title,
                    'description': submission.selftext[:500] if submission.selftext else submission.title,
                    'url': f"https://reddit.com{submission.permalink}",
                    'source': f"Reddit - r/{subreddit_name}",
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'subreddit': subreddit_name,
                    'published_date': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'category': 'Reddit Discussion',
                    'upvote_ratio': submission.upvote_ratio,
                    'is_relevant': True,
                    'relevance_score': round(relevance_score, 1),
                    'is_state_specific': False,  # Reddit posts are not state-specific
                    'status': 'pending_review',
                    'scraped_at': datetime.now().isoformat(),
                }

                posts.append(post)
            
            log.info(f"✅ Got {len(posts)} hot posts from r/{subreddit_name}")
            
        except Exception as e:
            log.error(f"❌ Error getting hot posts from r/{subreddit_name}: {e}")
        
        return posts

