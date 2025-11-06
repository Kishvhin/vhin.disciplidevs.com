#!/usr/bin/env python3
"""
NDTA News Pipeline - Web Dashboard
Simple Flask web interface to view and manage the news pipeline
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import json
from pathlib import Path
from datetime import datetime
import subprocess
import os

app = Flask(__name__)

# Serve graphics as static files
@app.route('/static/graphics/<path:filename>')
def serve_graphic(filename):
    """Serve graphics from data/graphics directory"""
    graphics_dir = Path("data/graphics")
    return send_from_directory(graphics_dir, filename)

# Data directories
RAW_NEWS_DIR = Path("data/raw_news")
PROCESSED_NEWS_DIR = Path("data/processed_news")
GRAPHICS_DIR = Path("data/graphics")
APPROVED_DIR = Path("data/approved_content")

def load_json_files(directory):
    """Load all JSON files from a directory"""
    files = []
    if directory.exists():
        for file in directory.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle both single objects and arrays
                    if isinstance(data, list):
                        # If it's an array, add each item separately
                        for item in data:
                            if isinstance(item, dict):
                                item['filename'] = file.name
                                files.append(item)
                    elif isinstance(data, dict):
                        # If it's a single object, add it directly
                        data['filename'] = file.name
                        files.append(data)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    return files

def get_pipeline_status():
    """Get current pipeline status"""
    raw_articles = load_json_files(RAW_NEWS_DIR)
    processed_reports = load_json_files(PROCESSED_NEWS_DIR)
    approved_content = load_json_files(APPROVED_DIR)
    
    unreviewed = [a for a in raw_articles if a.get('status') == 'pending_review']
    approved_for_processing = [a for a in raw_articles if a.get('status') == 'approved']
    needing_graphics = [r for r in processed_reports if r.get('status') == 'pending_graphics']
    pending_approval = [r for r in processed_reports if r.get('status') == 'pending_approval']
    ready_to_post = [c for c in approved_content if c.get('status') == 'approved' and not c.get('posted')]
    
    return {
        'unreviewed': len(unreviewed),
        'approved_for_processing': len(approved_for_processing),
        'needing_graphics': len(needing_graphics),
        'pending_approval': len(pending_approval),
        'ready_to_post': len(ready_to_post),
        'total_articles': len(raw_articles),
        'total_reports': len(processed_reports),
        'total_approved': len(approved_content)
    }

@app.route('/')
def index():
    """Dashboard home page"""
    status = get_pipeline_status()
    return render_template('dashboard.html', status=status)

@app.route('/articles')
def articles():
    """View all scraped articles"""
    raw_articles = load_json_files(RAW_NEWS_DIR)
    # Sort by date, newest first
    raw_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
    return render_template('articles.html', articles=raw_articles)

@app.route('/reports')
def reports():
    """View all generated reports"""
    processed_reports = load_json_files(PROCESSED_NEWS_DIR)
    processed_reports.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return render_template('reports.html', reports=processed_reports)

@app.route('/approved')
def approved():
    """View approved content ready to post"""
    approved_content = load_json_files(APPROVED_DIR)
    approved_content.sort(key=lambda x: x.get('approved_at', ''), reverse=True)
    return render_template('approved.html', content=approved_content)

@app.route('/workflow')
def workflow():
    """View workflow visualization"""
    return render_template('workflow.html')

@app.route('/graphics')
def graphics():
    """View graphics gallery"""
    graphics_list = []
    if GRAPHICS_DIR.exists():
        for file in GRAPHICS_DIR.glob("*.png"):
            # Try to find matching report
            graphic_id = file.stem.replace('graphic_', '')
            title = "NDTA News Graphic"

            # Look for matching report
            for report_file in PROCESSED_NEWS_DIR.glob("*.json"):
                try:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report = json.load(f)
                        if report.get('graphic_path') and graphic_id in report.get('graphic_path', ''):
                            title = report.get('headline', title)
                            break
                except:
                    pass

            graphics_list.append({
                'filename': file.name,
                'title': title,
                'created_at': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    graphics_list.sort(key=lambda x: x['created_at'], reverse=True)
    return render_template('graphics.html', graphics=graphics_list)

@app.route('/api/status')
def api_status():
    """API endpoint for status"""
    return jsonify(get_pipeline_status())

@app.route('/api/workflow')
def api_workflow():
    """API endpoint for workflow data"""
    status = get_pipeline_status()

    # Add graphics count
    graphics_count = 0
    if GRAPHICS_DIR.exists():
        graphics_count = len(list(GRAPHICS_DIR.glob("*.png")))

    # Get sample graphics
    sample_graphics = []
    if GRAPHICS_DIR.exists():
        for file in list(GRAPHICS_DIR.glob("*.png"))[:3]:
            sample_graphics.append(file.name)

    return jsonify({
        **status,
        'graphics_count': graphics_count,
        'sample_graphics': sample_graphics
    })

@app.route('/api/article/<article_id>')
def api_article(article_id):
    """Get single article details"""
    raw_articles = load_json_files(RAW_NEWS_DIR)
    article = next((a for a in raw_articles if a.get('id') == article_id), None)
    if article:
        return jsonify(article)
    return jsonify({'error': 'Article not found'}), 404

@app.route('/api/approve/<article_id>', methods=['POST'])
def api_approve_article(article_id):
    """Approve an article for processing"""
    file_path = RAW_NEWS_DIR / f"article_{article_id}.json"
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            article = json.load(f)
        article['status'] = 'approved'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2)
        return jsonify({'success': True})
    return jsonify({'error': 'Article not found'}), 404

@app.route('/api/reject/<article_id>', methods=['POST'])
def api_reject_article(article_id):
    """Reject an article"""
    file_path = RAW_NEWS_DIR / f"article_{article_id}.json"
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            article = json.load(f)
        article['status'] = 'rejected'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2)
        return jsonify({'success': True})
    return jsonify({'error': 'Article not found'}), 404

@app.route('/api/run/<command>', methods=['POST'])
def api_run_command(command):
    """Run pipeline commands"""
    allowed_commands = ['scrape', 'generate', 'graphics', 'post', 'auto']
    if command not in allowed_commands:
        return jsonify({'error': 'Invalid command'}), 400

    try:
        # For 'auto' command, run the full automated workflow
        if command == 'auto':
            return run_automated_workflow()

        result = subprocess.run(
            ['python', 'main.py', command],
            capture_output=True,
            text=True,
            timeout=300
        )
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_automated_workflow():
    """Run the full automated workflow: scrape → auto-approve verified → generate → graphics → post"""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    results = {
        'scrape': {'success': False, 'count': 0},
        'auto_approve': {'success': False, 'count': 0},
        'generate': {'success': False, 'count': 0},
        'graphics': {'success': False, 'count': 0},
        'post': {'success': False, 'count': 0},
        'errors': []
    }

    try:
        from scrapers.news_scraper import NewsScraper
        from content_generator.report_generator import ReportGenerator
        from graphics.graphic_generator import GraphicGenerator
        from distribution.social_poster import SocialPoster
    except ImportError as e:
        return jsonify({
            'success': False,
            'results': results,
            'error': f'Import error: {str(e)}. Please ensure all dependencies are installed.'
        }), 500

    try:
        # Step 1: Scrape
        scraper = NewsScraper()
        scrape_result = scraper.run_scrape()
        results['scrape'] = {'success': True, 'count': scrape_result.get('total', 0)}

        # Step 2: Load all scraped articles and auto-approve verified ones
        all_articles = load_json_files(RAW_NEWS_DIR)
        auto_approved = 0

        for article in all_articles:
            # Auto-approve if verification score is high and relevance is high
            verification = article.get('verification', {})
            if (verification.get('recommendation') == 'auto_approve' and
                article.get('relevance_score', 0) >= 8 and
                article.get('status') == 'pending_review'):

                article['status'] = 'approved'
                article['approved_at'] = datetime.now().isoformat()

                # Find and update the original file
                for file in RAW_NEWS_DIR.glob("*.json"):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Handle both single objects and arrays
                            if isinstance(data, list):
                                for i, item in enumerate(data):
                                    if item.get('id') == article['id']:
                                        data[i] = article
                                        with open(file, 'w', encoding='utf-8') as fw:
                                            json.dump(data, fw, indent=2)
                                        auto_approved += 1
                                        break
                            elif isinstance(data, dict) and data.get('id') == article['id']:
                                with open(file, 'w', encoding='utf-8') as fw:
                                    json.dump(article, fw, indent=2)
                                auto_approved += 1
                                break
                    except:
                        pass

        results['auto_approve'] = {'success': True, 'count': auto_approved}

        # Step 3: Generate reports for approved articles
        generator = ReportGenerator()
        approved_articles = [a for a in all_articles if a.get('status') == 'approved']
        generated = 0
        for article in approved_articles:
            try:
                report = generator.generate_report(article)
                if report:
                    generated += 1
            except Exception as e:
                results['errors'].append(f"Generate error: {str(e)}")

        results['generate'] = {'success': True, 'count': generated}

        # Step 4: Create graphics
        graphic_gen = GraphicGenerator()
        reports = load_json_files(PROCESSED_NEWS_DIR)
        graphics_created = 0
        for report in reports:
            if not report.get('graphic_path'):
                try:
                    graphic_path = graphic_gen.create_graphic(report)
                    if graphic_path:
                        graphics_created += 1
                except Exception as e:
                    results['errors'].append(f"Graphics error: {str(e)}")

        results['graphics'] = {'success': True, 'count': graphics_created}

        # Step 5: Auto-approve and post
        poster = SocialPoster()
        approved_content = load_json_files(APPROVED_DIR)
        posted = 0
        for content in approved_content:
            if not content.get('posted'):
                try:
                    # Auto-approve if verification score is high
                    verification = content.get('verification', {})
                    if verification.get('overall_score', 0) >= 8:
                        success = poster.post_to_twitter(content)
                        if success:
                            content['posted'] = True
                            content['posted_at'] = datetime.now().isoformat()
                            # Save updated content
                            content_file = APPROVED_DIR / f"approved_{content['id']}.json"
                            with open(content_file, 'w', encoding='utf-8') as f:
                                json.dump(content, f, indent=2)
                            posted += 1
                except Exception as e:
                    results['errors'].append(f"Post error: {str(e)}")

        results['post'] = {'success': True, 'count': posted}

        return jsonify({
            'success': True,
            'results': results,
            'summary': f"Scraped {results['scrape']['count']}, Auto-approved {results['auto_approve']['count']}, Generated {results['generate']['count']}, Created {results['graphics']['count']} graphics, Posted {results['post']['count']}"
        })

    except Exception as e:
        results['errors'].append(str(e))
        return jsonify({
            'success': False,
            'results': results,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("\n" + "="*60)
    print("  🌐 NDTA NEWS PIPELINE - WEB DASHBOARD")
    print("="*60)
    print("\n  Starting web server...")
    print("  Open your browser to: http://localhost:5000")
    print("\n  Press CTRL+C to stop the server")
    print("="*60 + "\n")

    # Get port from environment variable (for cloud deployment) or use 5000
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') != 'production'

    app.run(debug=debug, host='0.0.0.0', port=port)

