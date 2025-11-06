#!/usr/bin/env python3
"""
Quick test to verify API keys are configured
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*60)
print("  🔍 CHECKING API KEY CONFIGURATION")
print("="*60)

# Check OpenAI
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key and openai_key != 'your_openai_api_key_here':
    print("✅ OpenAI API key configured")
else:
    print("❌ OpenAI API key NOT configured (REQUIRED)")

# Check NewsAPI
newsapi_key = os.getenv('NEWSAPI_KEY')
if newsapi_key and newsapi_key != 'your_newsapi_key_here':
    print("✅ NewsAPI key configured")
else:
    print("⚠️  NewsAPI key not configured (optional)")

# Check Twitter
twitter_keys = [
    ('TWITTER_API_KEY', 'Twitter API Key'),
    ('TWITTER_API_SECRET', 'Twitter API Secret'),
    ('TWITTER_ACCESS_TOKEN', 'Twitter Access Token'),
    ('TWITTER_ACCESS_SECRET', 'Twitter Access Secret'),
]

twitter_ok = True
for key, name in twitter_keys:
    value = os.getenv(key)
    if value and value != f'your_{key.lower()}_here':
        print(f"✅ {name} configured")
    else:
        print(f"❌ {name} NOT configured (REQUIRED)")
        twitter_ok = False

# Check Facebook
fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
fb_page = os.getenv('FACEBOOK_PAGE_ID')

if fb_token and fb_token != 'your_facebook_access_token_here':
    print("✅ Facebook Access Token configured")
else:
    print("❌ Facebook Access Token NOT configured (REQUIRED)")

if fb_page and fb_page != 'your_facebook_page_id_here':
    print("✅ Facebook Page ID configured")
else:
    print("❌ Facebook Page ID NOT configured (REQUIRED)")

# Check Email
smtp_user = os.getenv('SMTP_USERNAME')
if smtp_user and smtp_user != 'your_email@gmail.com':
    print("✅ Email alerts configured")
else:
    print("⚠️  Email alerts not configured (optional)")

print("\n" + "="*60)

# Summary
required_ok = (
    openai_key and openai_key != 'your_openai_api_key_here' and
    twitter_ok and
    fb_token and fb_token != 'your_facebook_access_token_here' and
    fb_page and fb_page != 'your_facebook_page_id_here'
)

if required_ok:
    print("🎉 ALL REQUIRED API KEYS CONFIGURED!")
    print("\nYou're ready to run:")
    print("  python main.py scrape")
else:
    print("⚠️  SOME REQUIRED API KEYS ARE MISSING")
    print("\nPlease edit .env file and add:")
    if not (openai_key and openai_key != 'your_openai_api_key_here'):
        print("  - OpenAI API key")
    if not twitter_ok:
        print("  - Twitter API keys (all 4)")
    if not (fb_token and fb_token != 'your_facebook_access_token_here'):
        print("  - Facebook Access Token")
    if not (fb_page and fb_page != 'your_facebook_page_id_here'):
        print("  - Facebook Page ID")

print("="*60 + "\n")

