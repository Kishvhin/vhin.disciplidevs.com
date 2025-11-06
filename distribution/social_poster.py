"""
Social Media Poster for NDTA News Pipeline
Posts to Twitter and Facebook
"""
import logging
from pathlib import Path
from typing import Dict
import tweepy
import requests

import utils.config_loader as config

log = logging.getLogger(__name__)


class SocialPoster:
    """Posts content to social media platforms"""
    
    def __init__(self):
        self.config = config.load_config()
        self.env = self.config['env']
        
        # Initialize Twitter client
        self.twitter_client = self._init_twitter()
        
        # Facebook config
        self.facebook_token = self.env.get('facebook_access_token')
        self.facebook_page_id = self.env.get('facebook_page_id')
    
    def _init_twitter(self):
        """Initialize Twitter API client"""
        try:
            # Twitter API v2 with OAuth 1.0a
            client = tweepy.Client(
                consumer_key=self.env.get('twitter_api_key'),
                consumer_secret=self.env.get('twitter_api_secret'),
                access_token=self.env.get('twitter_access_token'),
                access_token_secret=self.env.get('twitter_access_secret')
            )
            
            # Also need v1.1 API for media upload
            auth = tweepy.OAuth1UserHandler(
                self.env.get('twitter_api_key'),
                self.env.get('twitter_api_secret'),
                self.env.get('twitter_access_token'),
                self.env.get('twitter_access_secret')
            )
            self.twitter_api_v1 = tweepy.API(auth)
            
            log.info("Twitter client initialized")
            return client
            
        except Exception as e:
            log.error(f"Error initializing Twitter client: {e}")
            return None
    
    def post_to_twitter(self, content: Dict) -> Dict:
        """Post content to Twitter"""
        
        if not self.twitter_client:
            log.warning("Twitter not configured")
            return {'success': False, 'error': 'Twitter not configured'}
        
        try:
            # Upload media if graphic exists
            media_id = None
            if content.get('graphic_path'):
                graphic_path = Path(content['graphic_path'])
                if graphic_path.exists():
                    media = self.twitter_api_v1.media_upload(str(graphic_path))
                    media_id = media.media_id
                    log.info(f"Media uploaded to Twitter: {media_id}")
            
            # Post tweet
            tweet_text = content['social_text']
            
            if media_id:
                response = self.twitter_client.create_tweet(
                    text=tweet_text,
                    media_ids=[media_id]
                )
            else:
                response = self.twitter_client.create_tweet(text=tweet_text)
            
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"
            
            log.info(f"Posted to Twitter: {tweet_url}")
            
            return {
                'success': True,
                'platform': 'twitter',
                'url': tweet_url,
                'tweet_id': tweet_id
            }
            
        except Exception as e:
            log.error(f"Error posting to Twitter: {e}", exc_info=True)
            return {
                'success': False,
                'platform': 'twitter',
                'error': str(e)
            }
    
    def post_to_facebook(self, content: Dict) -> Dict:
        """Post content to Facebook page"""
        
        if not self.facebook_token or not self.facebook_page_id:
            log.warning("Facebook not configured")
            return {'success': False, 'error': 'Facebook not configured'}
        
        try:
            # Facebook Graph API endpoint
            url = f"https://graph.facebook.com/v18.0/{self.facebook_page_id}/feed"
            
            # Prepare post data
            post_data = {
                'message': f"{content['headline']}\n\n{content['summary']}\n\n{content['social_text']}",
                'access_token': self.facebook_token
            }
            
            # Add photo if graphic exists
            if content.get('graphic_path'):
                graphic_path = Path(content['graphic_path'])
                if graphic_path.exists():
                    # Upload photo
                    photo_url = f"https://graph.facebook.com/v18.0/{self.facebook_page_id}/photos"
                    
                    with open(graphic_path, 'rb') as image_file:
                        files = {'source': image_file}
                        photo_data = {
                            'message': post_data['message'],
                            'access_token': self.facebook_token
                        }
                        
                        response = requests.post(photo_url, data=photo_data, files=files)
                        response.raise_for_status()
                        result = response.json()
                        
                        post_id = result.get('id', result.get('post_id'))
                        
                        log.info(f"Posted to Facebook with photo: {post_id}")
                        
                        return {
                            'success': True,
                            'platform': 'facebook',
                            'post_id': post_id,
                            'url': f"https://facebook.com/{post_id}"
                        }
            
            # Post without photo
            response = requests.post(url, data=post_data)
            response.raise_for_status()
            result = response.json()
            
            post_id = result.get('id')
            
            log.info(f"Posted to Facebook: {post_id}")
            
            return {
                'success': True,
                'platform': 'facebook',
                'post_id': post_id,
                'url': f"https://facebook.com/{post_id}"
            }
            
        except Exception as e:
            log.error(f"Error posting to Facebook: {e}", exc_info=True)
            return {
                'success': False,
                'platform': 'facebook',
                'error': str(e)
            }
    
    def post_to_facebook_group(self, content: Dict, group_id: str) -> Dict:
        """Post content to a specific Facebook group"""
        
        if not self.facebook_token:
            log.warning("Facebook not configured")
            return {'success': False, 'error': 'Facebook not configured'}
        
        try:
            url = f"https://graph.facebook.com/v18.0/{group_id}/feed"
            
            post_data = {
                'message': f"📍 {content.get('state', '')} NEWS\n\n{content['headline']}\n\n{content['summary']}",
                'access_token': self.facebook_token
            }
            
            response = requests.post(url, data=post_data)
            response.raise_for_status()
            result = response.json()
            
            post_id = result.get('id')
            
            log.info(f"Posted to Facebook group {group_id}: {post_id}")
            
            return {
                'success': True,
                'platform': 'facebook_group',
                'group_id': group_id,
                'post_id': post_id
            }
            
        except Exception as e:
            log.error(f"Error posting to Facebook group: {e}", exc_info=True)
            return {
                'success': False,
                'platform': 'facebook_group',
                'error': str(e)
            }
    
    def post_to_all_platforms(self, content: Dict) -> Dict:
        """Post to all configured platforms"""
        
        results = {
            'success': False,
            'platforms': []
        }
        
        # Post to Twitter
        twitter_result = self.post_to_twitter(content)
        results['platforms'].append(twitter_result)
        
        if twitter_result['success']:
            results['twitter_url'] = twitter_result['url']
        
        # Post to Facebook
        facebook_result = self.post_to_facebook(content)
        results['platforms'].append(facebook_result)
        
        if facebook_result['success']:
            results['facebook_url'] = facebook_result['url']
        
        # Check if at least one succeeded
        results['success'] = any(p['success'] for p in results['platforms'])
        
        if results['success']:
            results['message'] = 'Posted successfully to at least one platform'
        else:
            results['message'] = 'Failed to post to all platforms'
        
        return results

