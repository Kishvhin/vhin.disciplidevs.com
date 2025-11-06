# New News Sources Guide

## 🎉 New Features Added

The NDTA News Pipeline now includes **two powerful new sources** for dump truck industry information:

### 1. 🗨️ Reddit Scraper
Monitors dump truck conversations and discussions across Reddit

### 2. 🏛️ State DOT Scraper
Tracks Department of Transportation news from all 50 states

---

## 📱 Reddit Scraper

### What It Does
- Monitors 10+ relevant subreddits for dump truck discussions
- Searches Reddit for specific dump truck keywords
- Captures real conversations from truck drivers and operators
- Filters for relevance and engagement (upvotes, comments)

### Monitored Subreddits
- r/Truckers
- r/trucking
- r/Construction
- r/heavyequipment
- r/CommercialTrucking
- r/OwnerOperators
- r/Diesel
- r/mechanics
- r/smallbusiness
- r/Entrepreneur

### Search Keywords
- "dump truck"
- "dump trailer"
- "tipper truck"
- "aggregate hauling"
- "material hauling"
- "vocational truck"

### Configuration
Edit `config/news_sources.yaml` to customize:

```yaml
reddit:
  enabled: true
  
  # Add/remove subreddits
  subreddits:
    - "Truckers"
    - "trucking"
    # ... add more
  
  # Add/remove keywords
  keywords:
    - "dump truck"
    # ... add more
  
  # Quality filters
  min_score: 5        # Minimum upvotes
  min_comments: 2     # Minimum comments
```

### What You Get
Each Reddit post includes:
- **Title** - Post title
- **Description** - Post content (first 500 chars)
- **URL** - Link to discussion
- **Source** - Which subreddit (e.g., "Reddit - r/Truckers")
- **Author** - Reddit username
- **Score** - Upvotes minus downvotes
- **Comments** - Number of comments
- **Published Date** - When posted

### Use Cases
- **Real operator feedback** - What are dump truck operators actually saying?
- **Problem discovery** - What issues are they facing?
- **Market research** - What are they buying/selling?
- **Trend spotting** - What's being discussed right now?

---

## 🏛️ State DOT Scraper

### What It Does
- Monitors Department of Transportation websites from all 50 states
- Tracks regulations, permits, road restrictions, and infrastructure news
- Prioritizes key states (Georgia, Florida, etc.)
- Captures state-specific trucking regulations

### Coverage
All 50 states configured with:
- Official DOT website URLs
- RSS feeds (where available)
- Web scraping fallback

### Priority States
Default priority states (checked first):
- **GA** - Georgia (NDTA home state)
- **FL** - Florida
- **AL** - Alabama
- **SC** - South Carolina
- **NC** - North Carolina
- **TN** - Tennessee
- **TX** - Texas
- **CA** - California

### Configuration
Edit `config/news_sources.yaml`:

```yaml
dot_sources:
  enabled: true
  
  # Priority states to check first
  priority_states:
    - "GA"
    - "FL"
    - "TX"
    # ... add more
  
  # Check all 50 states
  check_all_states: true
  
  # How often to check
  check_frequency: "daily"
  
  # Topics of interest
  relevant_topics:
    - "truck regulations"
    - "weight limits"
    - "permits"
    - "road restrictions"
    - "construction projects"
    - "infrastructure funding"
    - "safety regulations"
    - "emissions standards"
    - "toll roads"
    - "bridge restrictions"
```

### What You Get
Each DOT article includes:
- **Title** - News headline
- **Description** - Article summary
- **URL** - Link to full article
- **Source** - State DOT name (e.g., "Georgia DOT")
- **State** - State code (e.g., "GA")
- **Category** - "DOT_News"
- **Published Date** - When published

### Use Cases
- **Regulatory alerts** - New truck regulations by state
- **Permit changes** - Updated permit requirements
- **Road restrictions** - Weight limits, bridge closures
- **Infrastructure news** - Construction projects affecting routes
- **State-specific alerts** - Trigger alerts for Georgia members

---

## 🚀 How to Use

### 1. Automatic Integration
The new sources are **automatically included** in the main scraping workflow:

```bash
# Run the full pipeline (includes Reddit + DOT)
python main.py scrape
```

Or use the web dashboard:
- Click **"🚀 Run Full Automated Workflow"**
- Reddit and DOT sources are scraped automatically

### 2. Test the New Sources
Run the test script to verify everything works:

```bash
python test_new_sources.py
```

This will:
- Test Reddit scraping
- Test DOT scraping
- Show sample results
- Display statistics

### 3. Manual Testing
Test individual scrapers:

```python
from scrapers.reddit_scraper import RedditScraper
from scrapers.dot_scraper import DOTScraper
import utils.config_loader as config

# Test Reddit
cfg = config.load_config()
reddit = RedditScraper(cfg)
posts = reddit.scrape_all(lookback_days=7)
print(f"Found {len(posts)} Reddit posts")

# Test DOT
dot = DOTScraper(cfg)
articles = dot.scrape_all_states(lookback_days=7, priority_states=['GA', 'FL'])
print(f"Found {len(articles)} DOT articles")
```

---

## 📊 Expected Results

### Reddit Scraper
- **Volume**: 100-300 posts per week
- **Quality**: Real operator discussions and questions
- **Engagement**: Posts with 5+ upvotes and 2+ comments
- **Relevance**: Filtered for dump truck keywords

### DOT Scraper
- **Volume**: 10-50 articles per week (from priority states)
- **Quality**: Official government announcements
- **Timeliness**: Latest regulatory changes
- **Coverage**: All 50 states available

---

## ⚙️ Technical Details

### Files Added
- `scrapers/reddit_scraper.py` - Reddit scraping logic
- `scrapers/dot_scraper.py` - DOT scraping logic
- `test_new_sources.py` - Test script for new sources

### Files Modified
- `scrapers/news_scraper.py` - Integrated new scrapers
- `config/news_sources.yaml` - Added Reddit and DOT configuration

### Dependencies
No new dependencies required! Uses existing libraries:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing (for DOT sites)

### Rate Limiting
Both scrapers include rate limiting to be respectful:
- **Reddit**: 2-second delay between requests
- **DOT**: 1-second delay between states

---

## 🎯 Next Steps

### 1. Customize Configuration
Edit `config/news_sources.yaml` to:
- Add/remove subreddits
- Adjust keywords
- Change priority states
- Modify quality filters

### 2. Run a Test Scrape
```bash
python test_new_sources.py
```

### 3. Run Full Pipeline
```bash
python main.py scrape
```
Or use the web dashboard at http://localhost:5000

### 4. Review Results
Check the dashboard for:
- Reddit discussions in the articles feed
- DOT news marked with state codes
- State-specific alerts for Georgia content

---

## 💡 Tips

### For Reddit
- **Best times**: Scrape daily to catch fresh discussions
- **Engagement**: Posts with more comments = more valuable insights
- **Subreddits**: Add industry-specific subreddits as you discover them

### For DOT
- **Priority states**: Focus on states where NDTA has members
- **Frequency**: Daily checks for regulatory changes
- **Alerts**: Set up state-specific alerts for Georgia members

### For Both
- **Lookback period**: 7 days is good for daily scraping
- **Relevance**: AI will still filter for dump truck relevance
- **Verification**: High-quality posts/articles get auto-approved

---

## 🐛 Troubleshooting

### Reddit Returns 403 Errors
- **Normal**: Reddit rate-limits requests
- **Solution**: Scraper automatically continues with other sources
- **Tip**: Spread out scraping over time

### DOT Scraper Returns 0 Articles
- **Reason**: Each state DOT has different HTML structure
- **Current**: Basic web scraping implemented
- **Future**: Can add state-specific parsers as needed
- **Alternative**: Many states have RSS feeds (configured)

### Too Many Results
Adjust filters in `config/news_sources.yaml`:
```yaml
reddit:
  min_score: 10      # Increase for higher quality
  min_comments: 5    # Increase for more discussion
```

---

## 📈 Success Metrics

After running for a week, you should see:
- ✅ 100+ Reddit posts captured
- ✅ Real operator conversations in the feed
- ✅ State DOT news from priority states
- ✅ Increased content variety
- ✅ Better industry coverage

---

## 🎉 Summary

You now have **two powerful new sources** feeding your NDTA news pipeline:

1. **Reddit** - Real conversations from dump truck operators
2. **State DOTs** - Official regulatory news from all 50 states

Both are:
- ✅ Fully integrated into the main workflow
- ✅ Automatically filtered for relevance
- ✅ Configured and ready to use
- ✅ Tested and working

**Just run the pipeline and watch the new content flow in!** 🚀

