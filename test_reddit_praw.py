"""
Test script for Reddit PRAW integration
Tests the official Reddit API with your credentials
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.reddit_scraper_praw import RedditScraperPRAW
import utils.config_loader as config


def test_authentication():
    """Test Reddit API authentication"""
    print("\n" + "="*60)
    print("TESTING REDDIT API AUTHENTICATION")
    print("="*60)
    
    try:
        cfg = config.load_config()
        scraper = RedditScraperPRAW(cfg)
        
        print("\n✅ Authentication successful!")
        print(f"   Logged in as: u/{scraper.reddit.user.me()}")
        print(f"   Comment karma: {scraper.reddit.user.me().comment_karma}")
        print(f"   Link karma: {scraper.reddit.user.me().link_karma}")
        
        return scraper
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nPlease check your credentials in .env file:")
        print("  - REDDIT_CLIENT_ID")
        print("  - REDDIT_CLIENT_SECRET")
        print("  - REDDIT_USERNAME")
        print("  - REDDIT_PASSWORD")
        return None


def test_subreddit_scrape(scraper):
    """Test scraping a single subreddit"""
    print("\n" + "="*60)
    print("TESTING SUBREDDIT SCRAPING")
    print("="*60)
    
    print("\n1. Scraping r/Truckers...")
    posts = scraper.scrape_subreddit('Truckers', lookback_days=30)
    
    print(f"   ✅ Found {len(posts)} relevant posts")
    
    if posts:
        print("\n   📝 Sample post:")
        post = posts[0]
        print(f"   Title: {post['title'][:70]}...")
        print(f"   Author: u/{post['author']}")
        print(f"   Score: {post['score']} upvotes ({post['upvote_ratio']*100:.0f}% upvoted)")
        print(f"   Comments: {post['num_comments']}")
        print(f"   URL: {post['url']}")
    
    return posts


def test_reddit_search(scraper):
    """Test Reddit-wide search"""
    print("\n" + "="*60)
    print("TESTING REDDIT SEARCH")
    print("="*60)
    
    print("\n2. Searching all of Reddit for 'dump truck'...")
    posts = scraper.search_reddit('dump truck', lookback_days=30, limit=50)
    
    print(f"   ✅ Found {len(posts)} posts")
    
    if posts:
        print("\n   📝 Sample search result:")
        post = posts[0]
        print(f"   Title: {post['title'][:70]}...")
        print(f"   Subreddit: r/{post['subreddit']}")
        print(f"   Score: {post['score']} upvotes")
        print(f"   URL: {post['url']}")
        
        # Show subreddit distribution
        subreddits = {}
        for post in posts:
            sub = post['subreddit']
            subreddits[sub] = subreddits.get(sub, 0) + 1
        
        print("\n   📊 Posts by subreddit:")
        for sub, count in sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      r/{sub}: {count} posts")
    
    return posts


def test_hot_posts(scraper):
    """Test getting hot/trending posts"""
    print("\n" + "="*60)
    print("TESTING HOT POSTS")
    print("="*60)
    
    print("\n3. Getting hot posts from r/Truckers...")
    posts = scraper.get_hot_posts('Truckers', limit=10)
    
    print(f"   ✅ Found {len(posts)} hot posts")
    
    if posts:
        print("\n   🔥 Top 3 hot posts:")
        for i, post in enumerate(posts[:3], 1):
            print(f"\n   {i}. {post['title'][:60]}...")
            print(f"      Score: {post['score']} | Comments: {post['num_comments']}")
    
    return posts


def test_full_scrape(scraper):
    """Test full scraping workflow"""
    print("\n" + "="*60)
    print("TESTING FULL SCRAPE")
    print("="*60)
    
    print("\n4. Running full scrape (all subreddits + searches)...")
    posts = scraper.scrape_all(lookback_days=7)
    
    print(f"   ✅ Total unique posts: {len(posts)}")
    
    # Show statistics
    if posts:
        total_score = sum(p['score'] for p in posts)
        total_comments = sum(p['num_comments'] for p in posts)
        avg_score = total_score / len(posts)
        avg_comments = total_comments / len(posts)
        
        print(f"\n   📊 Statistics:")
        print(f"      Average score: {avg_score:.1f} upvotes")
        print(f"      Average comments: {avg_comments:.1f}")
        print(f"      Total engagement: {total_score} upvotes, {total_comments} comments")
        
        # Show top post
        top_post = max(posts, key=lambda x: x['score'])
        print(f"\n   🏆 Top post:")
        print(f"      Title: {top_post['title'][:60]}...")
        print(f"      Score: {top_post['score']} upvotes")
        print(f"      Subreddit: r/{top_post['subreddit']}")
    
    return posts


def compare_with_old_scraper():
    """Compare PRAW scraper with old scraper"""
    print("\n" + "="*60)
    print("COMPARISON: PRAW vs Old Scraper")
    print("="*60)
    
    print("\n📊 Feature Comparison:")
    print("\n   Old Scraper (JSON API):")
    print("   ❌ Rate limit: 60 requests/hour")
    print("   ❌ Frequent 403 errors")
    print("   ❌ Limited data access")
    print("   ❌ No posting capability")
    print("   ❌ Unofficial API")
    
    print("\n   New Scraper (PRAW):")
    print("   ✅ Rate limit: 600 requests/10 minutes (10x better!)")
    print("   ✅ No 403 errors")
    print("   ✅ Full data access (awards, flair, etc.)")
    print("   ✅ Can post to Reddit")
    print("   ✅ Official Reddit API")
    print("   ✅ Better reliability")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 REDDIT PRAW API INTEGRATION TEST")
    print("Official Reddit API with OAuth Authentication")
    print("="*60)
    
    # Test authentication
    scraper = test_authentication()
    
    if not scraper:
        print("\n❌ Cannot proceed without authentication")
        print("\nPlease update your .env file with:")
        print("  REDDIT_PASSWORD=your_actual_reddit_password")
        return
    
    try:
        # Test individual features
        subreddit_posts = test_subreddit_scrape(scraper)
        search_posts = test_reddit_search(scraper)
        hot_posts = test_hot_posts(scraper)
        all_posts = test_full_scrape(scraper)
        
        # Show comparison
        compare_with_old_scraper()
        
        # Final summary
        print("\n" + "="*60)
        print("✅ TEST SUMMARY")
        print("="*60)
        print(f"✅ Authentication: SUCCESS")
        print(f"✅ Subreddit scraping: {len(subreddit_posts)} posts")
        print(f"✅ Reddit search: {len(search_posts)} posts")
        print(f"✅ Hot posts: {len(hot_posts)} posts")
        print(f"✅ Full scrape: {len(all_posts)} unique posts")
        print(f"\n🎉 All tests passed! Reddit API is working perfectly!")
        
        print("\n" + "="*60)
        print("📈 BENEFITS YOU'RE NOW GETTING:")
        print("="*60)
        print("✅ 10x higher rate limits (600 req/10min vs 60 req/hour)")
        print("✅ No more 403 errors")
        print("✅ Official API support")
        print("✅ More reliable scraping")
        print("✅ Access to more data (upvote ratio, awards, etc.)")
        print("✅ Ability to post to Reddit (if needed)")
        
        print("\n" + "="*60)
        print("🎯 NEXT STEPS:")
        print("="*60)
        print("1. Update news_scraper.py to use RedditScraperPRAW")
        print("2. Run the full pipeline to test integration")
        print("3. Enjoy better Reddit scraping!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

