#!/usr/bin/env python3
"""
Quick script to auto-approve all articles for testing
"""
import json
from pathlib import Path

RAW_NEWS_DIR = Path("data/raw_news")

approved_count = 0

# Find the scraped JSON file
for file in RAW_NEWS_DIR.glob("scraped_*.json"):
    with open(file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Approve all articles
    for article in articles:
        if article.get('status') == 'pending_review':
            article['status'] = 'approved'
            approved_count += 1
            print(f"✅ Approved: {article['title'][:70]}")

    # Save back
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)

print(f"\n✅ Total Approved: {approved_count}")

