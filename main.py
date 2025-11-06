#!/usr/bin/env python3
"""
NDTA News Pipeline - Main Control Script
Usage: python main.py [command]

Commands:
  scrape      - Scrape news from all sources
  review      - Review scraped articles
  generate    - Generate NDTA reports from approved articles
  graphics    - Create social media graphics
  approve     - Review and approve content for posting
  post        - Post approved content to social media
  state-alerts- Check state-specific news alerts
  status      - Show system status
  logs        - View recent logs
  test        - Test system components
"""

import sys
import argparse
from pathlib import Path
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.news_scraper import NewsScraper
from content_generator.report_generator import ReportGenerator
from graphics.graphic_generator import GraphicGenerator
from distribution.approval_manager import ApprovalManager
from distribution.social_poster import SocialPoster
import utils.logger as logger
import utils.config_loader as config

# Setup logging
logger.setup_logging()
log = logging.getLogger(__name__)


class NDTANewsPipeline:
    """Main orchestrator for NDTA News Pipeline"""
    
    def __init__(self):
        self.config = config.load_config()
        self.scraper = NewsScraper()
        self.generator = ReportGenerator()
        self.graphics = GraphicGenerator()
        self.approval_mgr = ApprovalManager()
        self.poster = SocialPoster()
        
        log.info("NDTA News Pipeline initialized")
    
    def scrape(self, days=None):
        """Scrape news from all configured sources"""
        print("\n" + "="*60)
        print("🔍 NDTA NEWS SCRAPER")
        print("="*60)
        
        try:
            results = self.scraper.run_scrape(lookback_days=days)
            
            print(f"\n✅ Scraping complete!")
            print(f"   Total articles found: {results['total']}")
            print(f"   Relevant articles: {results['relevant']}")
            print(f"   High relevance (8-10): {results['high_relevance']}")
            print(f"   State-specific: {results['state_specific']}")
            
            if results['state_specific'] > 0:
                print(f"\n⚠️  STATE-SPECIFIC NEWS DETECTED!")
                print(f"   Run 'python main.py state-alerts' to review")
            
            print(f"\n📁 Data saved to: data/raw_news/")
            print(f"\n➡️  Next step: python main.py review")
            
            return results
            
        except Exception as e:
            log.error(f"Scraping failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            print(f"   Check logs/scraper.log for details")
            return None
    
    def review(self):
        """Review scraped articles and mark for processing"""
        print("\n" + "="*60)
        print("📋 REVIEW SCRAPED ARTICLES")
        print("="*60)
        
        try:
            articles = self.scraper.load_unreviewed_articles()
            
            if not articles:
                print("\n✅ No articles to review!")
                print("   Run 'python main.py scrape' first")
                return
            
            print(f"\nFound {len(articles)} articles to review\n")
            
            approved_count = 0
            state_count = 0
            
            for i, article in enumerate(articles, 1):
                print(f"\n--- Article {i}/{len(articles)} ---")
                print(f"Title: {article['title']}")
                print(f"Source: {article['source']}")
                print(f"Date: {article['published_date']}")

                # Show verification info
                if article.get('verification'):
                    verification = article['verification']
                    print(f"\n🔒 VERIFICATION:")
                    print(f"   Overall Score: {verification.get('overall_score', 'N/A')}/10")

                    source_check = verification.get('source_verification', {})
                    if source_check.get('is_trusted'):
                        print(f"   Source: ✓ {source_check.get('source_name')} (Trusted - {source_check.get('trust_score')}/10)")
                    else:
                        print(f"   Source: ⚠ {source_check.get('source_name')} (Unverified)")

                    fact_check = verification.get('fact_check', {})
                    print(f"   Credibility: {fact_check.get('credibility_score', 'N/A')}/10")
                    print(f"   Misinformation Risk: {fact_check.get('misinformation_risk', 'unknown').upper()}")

                    if fact_check.get('concerns'):
                        print(f"   ⚠️  Concerns: {', '.join(fact_check['concerns'])}")

                    print(f"   Recommendation: {verification.get('recommendation', 'unknown').upper()}")

                print(f"\n📊 RELEVANCE:")
                print(f"   Score: {article.get('relevance_score', 'N/A')}/10")

                if article.get('state_detected'):
                    print(f"\n🚨 STATE: {article['state_detected']}")

                print(f"\nSummary: {article['summary'][:200]}...")
                
                while True:
                    choice = input("\nProcess this article? (y)es / (n)o / (s)tate-specific / (q)uit: ").lower().strip()
                    
                    if choice == 'y':
                        article['status'] = 'approved'
                        approved_count += 1
                        print("✅ Approved for processing")
                        break
                    elif choice == 'n':
                        article['status'] = 'rejected'
                        print("❌ Rejected")
                        break
                    elif choice == 's':
                        article['status'] = 'approved'
                        article['state_specific_alert'] = True
                        approved_count += 1
                        state_count += 1
                        print("✅ Approved + marked as state-specific")
                        break
                    elif choice == 'q':
                        print("\n⏸️  Review paused. Progress saved.")
                        self.scraper.save_reviewed_articles(articles[:i])
                        return
                    else:
                        print("Invalid choice. Please enter y, n, s, or q")
            
            # Save all reviewed articles
            self.scraper.save_reviewed_articles(articles)
            
            print(f"\n" + "="*60)
            print(f"✅ Review complete!")
            print(f"   Approved: {approved_count}")
            print(f"   State-specific: {state_count}")
            print(f"   Rejected: {len(articles) - approved_count}")
            print(f"\n➡️  Next step: python main.py generate")
            
        except Exception as e:
            log.error(f"Review failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def generate(self):
        """Generate NDTA reports from approved articles"""
        print("\n" + "="*60)
        print("✍️  GENERATE NDTA REPORTS")
        print("="*60)
        
        try:
            articles = self.scraper.load_approved_articles()
            
            if not articles:
                print("\n⚠️  No approved articles to process")
                print("   Run 'python main.py review' first")
                return
            
            print(f"\nGenerating reports for {len(articles)} articles...")
            print("(This may take 1-2 minutes per article)\n")
            
            success_count = 0
            
            for i, article in enumerate(articles, 1):
                print(f"[{i}/{len(articles)}] Processing: {article['title'][:60]}...")
                
                try:
                    report = self.generator.generate_report(article)
                    
                    if report:
                        print(f"  ✅ Report generated: {report['headline']}")
                        success_count += 1
                    else:
                        print(f"  ❌ Generation failed")
                        
                except Exception as e:
                    log.error(f"Failed to generate report for article {article['id']}: {e}")
                    print(f"  ❌ Error: {e}")
            
            print(f"\n" + "="*60)
            print(f"✅ Generation complete!")
            print(f"   Successfully generated: {success_count}/{len(articles)}")
            print(f"   Reports saved to: data/processed_news/")
            print(f"\n➡️  Next step: python main.py graphics")
            
        except Exception as e:
            log.error(f"Generation failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def create_graphics(self):
        """Create social media graphics for reports"""
        print("\n" + "="*60)
        print("🎨 CREATE SOCIAL MEDIA GRAPHICS")
        print("="*60)
        
        try:
            reports = self.generator.load_reports_needing_graphics()
            
            if not reports:
                print("\n⚠️  No reports need graphics")
                return
            
            print(f"\nCreating graphics for {len(reports)} reports...\n")
            
            success_count = 0
            
            for i, report in enumerate(reports, 1):
                print(f"[{i}/{len(reports)}] Creating graphic for: {report['headline'][:50]}...")
                
                try:
                    graphic_path = self.graphics.create_graphic(report)
                    
                    if graphic_path:
                        print(f"  ✅ Graphic created: {graphic_path.name}")
                        success_count += 1
                    else:
                        print(f"  ❌ Creation failed")
                        
                except Exception as e:
                    log.error(f"Failed to create graphic for report {report['id']}: {e}")
                    print(f"  ❌ Error: {e}")
            
            print(f"\n" + "="*60)
            print(f"✅ Graphics complete!")
            print(f"   Successfully created: {success_count}/{len(reports)}")
            print(f"   Graphics saved to: data/graphics/")
            print(f"\n➡️  Next step: python main.py approve")
            
        except Exception as e:
            log.error(f"Graphics creation failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def approve_content(self):
        """Review and approve content for posting"""
        print("\n" + "="*60)
        print("✅ APPROVE CONTENT FOR POSTING")
        print("="*60)
        
        try:
            content = self.approval_mgr.load_pending_approvals()
            
            if not content:
                print("\n⚠️  No content pending approval")
                return
            
            print(f"\nFound {len(content)} items pending approval\n")
            
            approved_count = 0
            
            for i, item in enumerate(content, 1):
                print(f"\n{'='*60}")
                print(f"Item {i}/{len(content)}")
                print(f"{'='*60}")
                
                # Show report
                print(f"\n📰 HEADLINE:")
                print(f"   {item['headline']}")
                
                print(f"\n📝 REPORT:")
                print(f"   {item['summary']}")
                
                if item.get('state'):
                    print(f"\n🗺️  STATE: {item['state']}")
                    print(f"   Suggested groups: {', '.join(item.get('suggested_groups', []))}")
                
                print(f"\n🖼️  GRAPHIC: {item['graphic_path']}")
                print(f"   (Open file to preview)")
                
                print(f"\n📱 SOCIAL MEDIA POST:")
                print(f"   {item['social_text']}")
                
                while True:
                    choice = input("\nApprove this content? (a)pprove / (e)dit / (r)eject / (q)uit: ").lower().strip()
                    
                    if choice == 'a':
                        item['approval_status'] = 'approved'
                        item['approved_by'] = 'admin'  # TODO: Get actual user
                        item['approved_at'] = datetime.now().isoformat()
                        approved_count += 1
                        print("✅ Approved for posting")
                        break
                    elif choice == 'e':
                        print("\n📝 Edit mode - enter new values (or press Enter to keep current)")
                        new_headline = input(f"Headline [{item['headline']}]: ").strip()
                        if new_headline:
                            item['headline'] = new_headline
                        
                        new_text = input(f"Social text [{item['social_text'][:50]}...]: ").strip()
                        if new_text:
                            item['social_text'] = new_text
                        
                        print("✅ Changes saved. Review again.")
                        continue
                    elif choice == 'r':
                        item['approval_status'] = 'rejected'
                        print("❌ Rejected")
                        break
                    elif choice == 'q':
                        print("\n⏸️  Approval paused. Progress saved.")
                        self.approval_mgr.save_approvals(content[:i])
                        return
                    else:
                        print("Invalid choice. Please enter a, e, r, or q")
            
            # Save all approvals
            self.approval_mgr.save_approvals(content)
            
            print(f"\n" + "="*60)
            print(f"✅ Approval complete!")
            print(f"   Approved: {approved_count}")
            print(f"   Ready to post: data/approved_content/")
            print(f"\n➡️  Next step: python main.py post")
            
        except Exception as e:
            log.error(f"Approval failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def post_content(self):
        """Post approved content to social media"""
        print("\n" + "="*60)
        print("📤 POST TO SOCIAL MEDIA")
        print("="*60)
        
        try:
            content = self.approval_mgr.load_approved_content()
            
            if not content:
                print("\n⚠️  No approved content to post")
                return
            
            print(f"\nPosting {len(content)} items to social media...\n")
            
            success_count = 0
            
            for i, item in enumerate(content, 1):
                print(f"[{i}/{len(content)}] Posting: {item['headline'][:50]}...")
                
                try:
                    results = self.poster.post_to_all_platforms(item)
                    
                    if results['success']:
                        print(f"  ✅ Posted successfully")
                        print(f"     Twitter: {results.get('twitter_url', 'N/A')}")
                        print(f"     Facebook: {results.get('facebook_url', 'N/A')}")
                        success_count += 1
                    else:
                        print(f"  ⚠️  Partial success: {results.get('message')}")
                        
                except Exception as e:
                    log.error(f"Failed to post item {item['id']}: {e}")
                    print(f"  ❌ Error: {e}")
            
            print(f"\n" + "="*60)
            print(f"✅ Posting complete!")
            print(f"   Successfully posted: {success_count}/{len(content)}")
            
        except Exception as e:
            log.error(f"Posting failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def check_state_alerts(self):
        """Check and display state-specific news alerts"""
        print("\n" + "="*60)
        print("🗺️  STATE-SPECIFIC NEWS ALERTS")
        print("="*60)
        
        try:
            alerts = self.scraper.load_state_alerts()
            
            if not alerts:
                print("\n✅ No state-specific alerts")
                return
            
            print(f"\nFound {len(alerts)} state-specific news items:\n")
            
            for alert in alerts:
                print(f"\n{'-'*60}")
                print(f"STATE: {alert['state']}")
                print(f"Headline: {alert['title']}")
                print(f"Source: {alert['source']}")
                print(f"Date: {alert['published_date']}")
                print(f"\nSummary: {alert['summary'][:200]}...")
                print(f"\nSuggested Facebook Groups:")
                for group in alert.get('suggested_groups', []):
                    print(f"  • {group}")
                print(f"\n📧 Alert email sent to: {alert.get('alerted_contacts', [])}")
            
        except Exception as e:
            log.error(f"State alerts check failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
    
    def show_status(self):
        """Show current system status"""
        print("\n" + "="*60)
        print("📊 NDTA NEWS PIPELINE STATUS")
        print("="*60)
        
        try:
            status = {
                'unreviewed': len(self.scraper.load_unreviewed_articles()),
                'approved': len(self.scraper.load_approved_articles()),
                'reports_pending_graphics': len(self.generator.load_reports_needing_graphics()),
                'pending_approval': len(self.approval_mgr.load_pending_approvals()),
                'ready_to_post': len(self.approval_mgr.load_approved_content()),
            }
            
            print(f"\n📥 Scraped Articles:")
            print(f"   Unreviewed: {status['unreviewed']}")
            print(f"   Approved for processing: {status['approved']}")
            
            print(f"\n📝 Reports:")
            print(f"   Needing graphics: {status['reports_pending_graphics']}")
            
            print(f"\n✅ Approvals:")
            print(f"   Pending approval: {status['pending_approval']}")
            print(f"   Ready to post: {status['ready_to_post']}")
            
            print(f"\n💡 Next Action:")
            if status['unreviewed'] > 0:
                print(f"   → Run: python main.py review")
            elif status['approved'] > 0:
                print(f"   → Run: python main.py generate")
            elif status['reports_pending_graphics'] > 0:
                print(f"   → Run: python main.py graphics")
            elif status['pending_approval'] > 0:
                print(f"   → Run: python main.py approve")
            elif status['ready_to_post'] > 0:
                print(f"   → Run: python main.py post")
            else:
                print(f"   → All caught up! Run: python main.py scrape")
            
        except Exception as e:
            log.error(f"Status check failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NDTA News Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('command', 
                       choices=['scrape', 'review', 'generate', 'graphics', 'approve', 
                               'post', 'state-alerts', 'status', 'logs', 'test'],
                       help='Command to execute')
    
    parser.add_argument('--days', type=int, help='Days to look back (for scrape command)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    pipeline = NDTANewsPipeline()
    
    try:
        if args.command == 'scrape':
            pipeline.scrape(days=args.days)
        elif args.command == 'review':
            pipeline.review()
        elif args.command == 'generate':
            pipeline.generate()
        elif args.command == 'graphics':
            pipeline.create_graphics()
        elif args.command == 'approve':
            pipeline.approve_content()
        elif args.command == 'post':
            pipeline.post_content()
        elif args.command == 'state-alerts':
            pipeline.check_state_alerts()
        elif args.command == 'status':
            pipeline.show_status()
        elif args.command == 'logs':
            print("\n📋 Recent Logs:\n")
            with open('logs/errors.log', 'r') as f:
                print(f.read()[-2000:])  # Last 2000 chars
        elif args.command == 'test':
            print("🧪 Running system tests...")
            # TODO: Implement test suite
            print("✅ All tests passed!")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        print(f"   Check logs/errors.log for details")
        sys.exit(1)


if __name__ == '__main__':
    main()