"""
Configuration loader for NDTA News Pipeline
"""
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """Load configuration from YAML and environment variables"""
    
    # Load environment variables
    load_dotenv()
    
    # Load YAML config
    config_path = Path("config/news_sources.yaml")
    
    if not config_path.exists():
        # Try alternate location
        config_path = Path("new_sources.ymal")
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    # Add environment variables
    config['env'] = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'newsapi_key': os.getenv('NEWSAPI_KEY'),
        'twitter_api_key': os.getenv('TWITTER_API_KEY'),
        'twitter_api_secret': os.getenv('TWITTER_API_SECRET'),
        'twitter_access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'twitter_access_secret': os.getenv('TWITTER_ACCESS_SECRET'),
        'facebook_access_token': os.getenv('FACEBOOK_ACCESS_TOKEN'),
        'facebook_page_id': os.getenv('FACEBOOK_PAGE_ID'),
        'reddit_client_id': os.getenv('REDDIT_CLIENT_ID'),
        'reddit_client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'reddit_user_agent': os.getenv('REDDIT_USER_AGENT', 'NDTA News Pipeline v1.0'),
        'reddit_username': os.getenv('REDDIT_USERNAME'),
        'reddit_password': os.getenv('REDDIT_PASSWORD'),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'smtp_username': os.getenv('SMTP_USERNAME'),
        'smtp_password': os.getenv('SMTP_PASSWORD'),
        'alert_email': os.getenv('ALERT_EMAIL'),
    }
    
    return config


def get_api_key(service):
    """Get API key for a specific service"""
    config = load_config()
    return config['env'].get(f'{service}_api_key')

