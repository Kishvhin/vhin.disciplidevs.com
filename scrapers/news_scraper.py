"""
Main News Scraper for NDTA News Pipeline
Coordinates all scraping and applies AI relevance filtering
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import hashlib
import openai
import time

from scrapers.rss_scraper import RSSFeedScraper
from scrapers.web_scraper import WebScraper
from scrapers.reddit_scraper_praw import RedditScraperPRAW
from scrapers.dot_scraper import DOTScraper
from scrapers.verification import ArticleVerifier
import utils.config_loader as config

log = logging.getLogger(__name__)


class NewsScraper:
    """Main news scraper with AI relevance filtering"""
    
    def __init__(self):
        self.config = config.load_config()
        self.rss_scraper = RSSFeedScraper(self.config)
        self.web_scraper = WebScraper(self.config)
        self.reddit_scraper = RedditScraperPRAW(self.config)  # Using official Reddit API
        self.dot_scraper = DOTScraper(self.config)
        self.verifier = ArticleVerifier(self.config)
        self.data_dir = Path("data/raw_news")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Setup OpenAI
        api_key = self.config['env'].get('openai_api_key')
        if api_key:
            openai.api_key = api_key
    
    def generate_article_id(self, article: Dict) -> str:
        """Generate unique ID for article"""
        unique_str = f"{article['title']}{article['url']}{article['source']}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:12]
    
    def check_relevance(self, article: Dict) -> Dict:
        """Use AI to check if article is relevant to dump truck industry"""
        
        prompt = f"""You are an expert in the dump truck and heavy-duty trucking industry.

Analyze this news article and determine:
1. Is it relevant to the dump truck industry? (Must directly help or affect dump truck businesses)
2. Relevance score (1-10, where 10 is highly relevant)
3. Brief reason for the score

Article:
Title: {article['title']}
Summary: {article['summary'][:500]}

Respond in JSON format:
{{
    "is_relevant": true/false,
    "relevance_score": 1-10,
    "reason": "brief explanation"
}}"""
        
        try:
            # Add delay to avoid rate limits
            time.sleep(1)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            log.error(f"Error checking relevance: {e}")
            # Default to manual review
            return {
                "is_relevant": True,
                "relevance_score": 5,
                "reason": "AI check failed, needs manual review"
            }
    
    def detect_state(self, article: Dict) -> Dict:
        """Detect if article is state-specific"""
        
        states = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
            'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
            'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
            'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
            'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
            'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
            'WI': 'Wisconsin', 'WY': 'Wyoming'
        }
        
        text = f"{article['title']} {article['summary']}".lower()
        
        detected_states = []
        for abbr, name in states.items():
            if name.lower() in text or f" {abbr.lower()} " in text:
                detected_states.append({'abbr': abbr, 'name': name})
        
        if detected_states:
            return {
                'is_state_specific': True,
                'states': detected_states,
                'confidence': 0.8
            }
        
        return {'is_state_specific': False, 'states': [], 'confidence': 0}
    
    def process_article(self, article: Dict) -> Dict:
        """Process a single article with AI filtering and verification"""

        # Generate ID
        article['id'] = self.generate_article_id(article)

        # STEP 1: Verify article legitimacy and quality
        log.info(f"Verifying: {article.get('title', 'Unknown')[:50]}...")
        verification = self.verifier.comprehensive_verification(article)

        # If verification fails, mark for rejection
        if verification['recommendation'] == 'reject':
            article['status'] = 'rejected'
            article['rejection_reason'] = 'Failed verification checks'
            article['processed_at'] = datetime.now().isoformat()
            log.warning(f"Article rejected: {article.get('title', 'Unknown')[:50]}")
            return article

        # STEP 2: Check relevance (only for verified articles)
        relevance = self.check_relevance(article)
        article['is_relevant'] = relevance['is_relevant']
        article['relevance_score'] = relevance['relevance_score']
        article['relevance_reason'] = relevance['reason']

        # STEP 3: Detect state
        state_info = self.detect_state(article)
        article['is_state_specific'] = state_info['is_state_specific']
        article['detected_states'] = state_info['states']

        # STEP 4: Set status based on verification and relevance
        if verification['recommendation'] == 'auto_approve' and article['relevance_score'] >= 8:
            article['status'] = 'auto_approved'
        else:
            article['status'] = 'pending_review'

        article['processed_at'] = datetime.now().isoformat()

        log.info(f"✓ Processed: Score={verification['overall_score']:.1f}, Relevance={article['relevance_score']}, Status={article['status']}")

        return article
    
    def run_scrape(self, lookback_days: int = None) -> Dict:
        """Run full scraping process"""
        
        if lookback_days is None:
            lookback_days = self.config.get('scraping', {}).get('lookback_days', 7)
        
        log.info(f"Starting news scrape (lookback: {lookback_days} days)")

        # Scrape from all sources
        articles = []

        # RSS feeds
        rss_articles = self.rss_scraper.scrape_all_feeds(lookback_days)
        articles.extend(rss_articles)
        log.info(f"  RSS: {len(rss_articles)} articles")

        # Web/NewsAPI
        web_articles = self.web_scraper.scrape_all(lookback_days)
        articles.extend(web_articles)
        log.info(f"  Web/NewsAPI: {len(web_articles)} articles")

        # Reddit discussions
        reddit_config = self.config.get('reddit', {})
        if reddit_config.get('enabled', True):
            reddit_articles = self.reddit_scraper.scrape_all(lookback_days)
            articles.extend(reddit_articles)
            log.info(f"  Reddit: {len(reddit_articles)} posts")

        # State DOT sources
        dot_config = self.config.get('dot_sources', {})
        if dot_config.get('enabled', True):
            priority_states = dot_config.get('priority_states', ['GA'])
            dot_articles = self.dot_scraper.scrape_all_states(lookback_days, priority_states)
            articles.extend(dot_articles)
            log.info(f"  DOT: {len(dot_articles)} articles")

        log.info(f"Total articles scraped: {len(articles)}")
        
        # Process each article with AI
        processed_articles = []
        relevant_count = 0
        high_relevance_count = 0
        state_specific_count = 0
        
        for article in articles:
            processed = self.process_article(article)
            processed_articles.append(processed)
            
            if processed['is_relevant']:
                relevant_count += 1
                if processed['relevance_score'] >= 8:
                    high_relevance_count += 1
            
            if processed['is_state_specific']:
                state_specific_count += 1
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.data_dir / f"scraped_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(processed_articles, f, indent=2)
        
        log.info(f"Saved {len(processed_articles)} articles to {output_file}")
        
        return {
            'total': len(processed_articles),
            'relevant': relevant_count,
            'high_relevance': high_relevance_count,
            'state_specific': state_specific_count,
            'output_file': str(output_file)
        }
    
    def load_unreviewed_articles(self) -> List[Dict]:
        """Load articles pending review"""
        articles = []
        
        for file in sorted(self.data_dir.glob("scraped_*.json")):
            with open(file, 'r') as f:
                data = json.load(f)
                for article in data:
                    if article.get('status') == 'pending_review' and article.get('is_relevant'):
                        articles.append(article)
        
        return articles
    
    def load_approved_articles(self) -> List[Dict]:
        """Load approved articles"""
        articles = []
        
        for file in sorted(self.data_dir.glob("scraped_*.json")):
            with open(file, 'r') as f:
                data = json.load(f)
                for article in data:
                    if article.get('status') == 'approved':
                        articles.append(article)
        
        return articles
    
    def save_reviewed_articles(self, articles: List[Dict]):
        """Save reviewed articles back to file"""
        # Group by original file
        by_file = {}
        for article in articles:
            # Find which file it came from
            for file in self.data_dir.glob("scraped_*.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                    if any(a['id'] == article['id'] for a in data):
                        if str(file) not in by_file:
                            by_file[str(file)] = data
                        # Update the article
                        for i, a in enumerate(by_file[str(file)]):
                            if a['id'] == article['id']:
                                by_file[str(file)][i] = article
                        break
        
        # Save back
        for file_path, data in by_file.items():
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    def load_state_alerts(self) -> List[Dict]:
        """Load state-specific articles"""
        articles = []
        
        for file in sorted(self.data_dir.glob("scraped_*.json")):
            with open(file, 'r') as f:
                data = json.load(f)
                for article in data:
                    if article.get('is_state_specific') and article.get('status') == 'approved':
                        articles.append(article)
        
        return articles

