"""
NDTA Report Generator
Transforms news articles into NDTA-branded reports
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import openai

from content_generator.prompts import (
    NDTA_VOICE, 
    REPORT_GENERATION_PROMPT,
    SOCIAL_POST_PROMPT
)
import utils.config_loader as config

log = logging.getLogger(__name__)


class ReportGenerator:
    """Generates NDTA-branded reports from news articles"""
    
    def __init__(self):
        self.config = config.load_config()
        self.output_dir = Path("data/processed_news")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup OpenAI
        api_key = self.config['env'].get('openai_api_key')
        if api_key:
            openai.api_key = api_key
        
        # Get AI settings
        ai_settings = self.config.get('ai_settings', {})
        self.model = ai_settings.get('model', 'gpt-4')
        self.temperature = ai_settings.get('temperature', 0.7)
        self.max_tokens = ai_settings.get('max_tokens', 1500)
    
    def generate_report(self, article: Dict) -> Dict:
        """Generate NDTA report from article"""
        
        log.info(f"Generating report for: {article['title']}")
        
        # Build prompt
        prompt = REPORT_GENERATION_PROMPT.format(
            ndta_voice=NDTA_VOICE,
            title=article['title'],
            source=article['source'],
            date=article.get('published_date', 'Recent'),
            content=f"{article['summary']}\n\n{article.get('content', '')}"[:2000]
        )
        
        try:
            # Call OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": NDTA_VOICE},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Try to extract JSON
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            report_data = json.loads(content.strip())
            
            # Generate social media post
            social_post = self.generate_social_post(report_data)
            
            # Build complete report
            report = {
                'id': article['id'],
                'original_article_id': article['id'],
                'headline': report_data['headline'],
                'executive_summary': report_data['executive_summary'],
                'key_facts': report_data['key_facts'],
                'industry_impact': report_data['industry_impact'],
                'ndta_perspective': report_data['ndta_perspective'],
                'action_items': report_data['action_items'],
                'call_to_action': report_data['call_to_action'],
                'social_post': social_post,
                'source_article': {
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source'],
                    'date': article.get('published_date')
                },
                'is_state_specific': article.get('is_state_specific', False),
                'detected_states': article.get('detected_states', []),
                'generated_at': datetime.now().isoformat(),
                'status': 'pending_graphics'
            }
            
            # Save report
            self.save_report(report)
            
            log.info(f"Report generated successfully: {report['headline']}")
            return report
            
        except Exception as e:
            log.error(f"Error generating report: {e}", exc_info=True)
            return None
    
    def generate_social_post(self, report_data: Dict) -> str:
        """Generate social media post from report"""
        
        prompt = SOCIAL_POST_PROMPT.format(
            ndta_voice=NDTA_VOICE,
            headline=report_data['headline'],
            summary=report_data['executive_summary']
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            log.error(f"Error generating social post: {e}")
            # Fallback
            return f"{report_data['headline']} #DumpTruck #Trucking #NDTA"
    
    def save_report(self, report: Dict):
        """Save report to file"""
        filename = f"report_{report['id']}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        log.info(f"Report saved to {filepath}")
    
    def load_reports_needing_graphics(self) -> List[Dict]:
        """Load reports that need graphics created"""
        reports = []
        
        for file in self.output_dir.glob("report_*.json"):
            with open(file, 'r') as f:
                report = json.load(f)
                if report.get('status') == 'pending_graphics':
                    reports.append(report)
        
        return reports
    
    def load_all_reports(self) -> List[Dict]:
        """Load all reports"""
        reports = []
        
        for file in sorted(self.output_dir.glob("report_*.json")):
            with open(file, 'r') as f:
                reports.append(json.load(f))
        
        return reports
    
    def update_report_status(self, report_id: str, status: str):
        """Update report status"""
        filepath = self.output_dir / f"report_{report_id}.json"
        
        if filepath.exists():
            with open(filepath, 'r') as f:
                report = json.load(f)
            
            report['status'] = status
            report['updated_at'] = datetime.now().isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)

