"""
Test script for new Reddit and DOT scrapers
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.reddit_scraper import RedditScraper
from scrapers.dot_scraper import DOTScraper
import utils.config_loader as config

def test_reddit_scraper():
    """Test Reddit scraper"""
    print("\n" + "="*60)
    print("TESTING REDDIT SCRAPER")
    print("="*60)
    
    cfg = config.load_config()
    scraper = RedditScraper(cfg)
    
    print("\n1. Testing single subreddit scrape (r/Truckers)...")
    posts = scraper.scrape_subreddit('Truckers', lookback_days=30)
    print(f"   Found {len(posts)} relevant posts")
    
    if posts:
        print("\n   Sample post:")
        post = posts[0]
        print(f"   Title: {post['title'][:80]}...")
        print(f"   URL: {post['url']}")
        print(f"   Score: {post['score']}, Comments: {post['num_comments']}")
    
    print("\n2. Testing Reddit search...")
    search_posts = scraper.search_reddit('dump truck', lookback_days=30)
    print(f"   Found {len(search_posts)} posts for 'dump truck'")
    
    if search_posts:
        print("\n   Sample search result:")
        post = search_posts[0]
        print(f"   Title: {post['title'][:80]}...")
        print(f"   Subreddit: r/{post['subreddit']}")
        print(f"   URL: {post['url']}")
    
    print("\n3. Testing full Reddit scrape...")
    all_posts = scraper.scrape_all(lookback_days=7)
    print(f"   Total unique posts: {len(all_posts)}")
    
    return all_posts

def test_dot_scraper():
    """Test DOT scraper"""
    print("\n" + "="*60)
    print("TESTING DOT SCRAPER")
    print("="*60)
    
    cfg = config.load_config()
    scraper = DOTScraper(cfg)
    
    print(f"\n1. Configured for {len(scraper.state_dots)} states")
    
    print("\n2. Testing Georgia DOT scrape...")
    ga_articles = scraper.scrape_state_dot('GA', lookback_days=30)
    print(f"   Found {len(ga_articles)} articles from Georgia DOT")
    
    if ga_articles:
        print("\n   Sample article:")
        article = ga_articles[0]
        print(f"   Title: {article['title'][:80]}...")
        print(f"   URL: {article['url']}")
        print(f"   Source: {article['source']}")
    
    print("\n3. Testing priority states scrape...")
    priority_states = ['GA', 'FL', 'AL']
    priority_articles = scraper.scrape_all_states(lookback_days=7, priority_states=priority_states)
    print(f"   Found {len(priority_articles)} total articles from {len(priority_states)} states")
    
    # Show breakdown by state
    state_counts = {}
    for article in priority_articles:
        state = article.get('state', 'Unknown')
        state_counts[state] = state_counts.get(state, 0) + 1
    
    print("\n   Breakdown by state:")
    for state, count in sorted(state_counts.items()):
        print(f"     {state}: {count} articles")
    
    return priority_articles

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("TESTING NEW NEWS SOURCES")
    print("Reddit & State DOT Scrapers")
    print("="*60)
    
    try:
        # Test Reddit
        reddit_posts = test_reddit_scraper()
        
        # Test DOT
        dot_articles = test_dot_scraper()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"✓ Reddit posts found: {len(reddit_posts)}")
        print(f"✓ DOT articles found: {len(dot_articles)}")
        print(f"✓ Total new sources: {len(reddit_posts) + len(dot_articles)}")
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

