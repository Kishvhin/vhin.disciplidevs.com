"""
Approval Manager for NDTA News Pipeline
Manages the approval workflow before posting
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import utils.config_loader as config

log = logging.getLogger(__name__)


class ApprovalManager:
    """Manages content approval workflow"""
    
    def __init__(self):
        self.config = config.load_config()
        self.pending_dir = Path("data/processed_news")
        self.approved_dir = Path("data/approved_content")
        self.approved_dir.mkdir(parents=True, exist_ok=True)
    
    def load_pending_approvals(self) -> List[Dict]:
        """Load content pending approval"""
        content = []
        
        for file in self.pending_dir.glob("report_*.json"):
            with open(file, 'r') as f:
                report = json.load(f)
                if report.get('status') == 'pending_approval':
                    # Format for approval review
                    item = {
                        'id': report['id'],
                        'headline': report['headline'],
                        'summary': report['executive_summary'],
                        'social_text': report['social_post'],
                        'graphic_path': report.get('graphic_path', ''),
                        'state': report['detected_states'][0]['name'] if report.get('is_state_specific') else None,
                        'suggested_groups': self._get_suggested_groups(report),
                        'full_report': report,
                        'approval_status': 'pending'
                    }
                    content.append(item)
        
        return content
    
    def _get_suggested_groups(self, report: Dict) -> List[str]:
        """Get suggested Facebook groups for state-specific content"""
        if not report.get('is_state_specific'):
            return []
        
        groups = []
        for state in report.get('detected_states', []):
            groups.extend(state.get('suggested_groups', []))
        
        return groups
    
    def save_approvals(self, content: List[Dict]):
        """Save approval decisions"""
        for item in content:
            if item.get('approval_status') == 'approved':
                # Move to approved directory
                approved_file = self.approved_dir / f"approved_{item['id']}.json"
                
                with open(approved_file, 'w') as f:
                    json.dump(item, f, indent=2)
                
                # Update original report status
                report_file = self.pending_dir / f"report_{item['id']}.json"
                if report_file.exists():
                    with open(report_file, 'r') as f:
                        report = json.load(f)
                    
                    report['status'] = 'approved'
                    report['approved_at'] = datetime.now().isoformat()
                    report['approved_by'] = item.get('approved_by', 'admin')
                    
                    with open(report_file, 'w') as f:
                        json.dump(report, f, indent=2)
                
                log.info(f"Content approved: {item['headline']}")
            
            elif item.get('approval_status') == 'rejected':
                # Update report status
                report_file = self.pending_dir / f"report_{item['id']}.json"
                if report_file.exists():
                    with open(report_file, 'r') as f:
                        report = json.load(f)
                    
                    report['status'] = 'rejected'
                    report['rejected_at'] = datetime.now().isoformat()
                    
                    with open(report_file, 'w') as f:
                        json.dump(report, f, indent=2)
                
                log.info(f"Content rejected: {item['headline']}")
    
    def load_approved_content(self) -> List[Dict]:
        """Load approved content ready for posting"""
        content = []
        
        for file in self.approved_dir.glob("approved_*.json"):
            with open(file, 'r') as f:
                item = json.load(f)
                if item.get('approval_status') == 'approved' and not item.get('posted'):
                    content.append(item)
        
        return content
    
    def mark_as_posted(self, content_id: str, platform_results: Dict):
        """Mark content as posted"""
        approved_file = self.approved_dir / f"approved_{content_id}.json"
        
        if approved_file.exists():
            with open(approved_file, 'r') as f:
                item = json.load(f)
            
            item['posted'] = True
            item['posted_at'] = datetime.now().isoformat()
            item['platform_results'] = platform_results
            
            with open(approved_file, 'w') as f:
                json.dump(item, f, indent=2)
            
            log.info(f"Marked as posted: {content_id}")
    
    def send_approval_notification(self, content: Dict):
        """Send email notification for approval"""
        
        smtp_config = self.config['env']
        
        if not smtp_config.get('smtp_username'):
            log.warning("Email not configured, skipping notification")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_config['smtp_username']
            msg['To'] = smtp_config.get('alert_email', smtp_config['smtp_username'])
            msg['Subject'] = f"NDTA News: Approval Needed - {content['headline']}"
            
            body = f"""
New NDTA news content is ready for approval:

HEADLINE: {content['headline']}

SUMMARY: {content['summary']}

SOCIAL POST: {content['social_text']}

STATE-SPECIFIC: {content.get('state', 'No')}

Please review and approve via the pipeline:
python main.py approve

---
NDTA News Pipeline
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['smtp_username'], smtp_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            log.info(f"Approval notification sent for: {content['headline']}")
            
        except Exception as e:
            log.error(f"Error sending approval notification: {e}")
    
    def send_state_alert(self, content: Dict):
        """Send alert for state-specific news"""
        
        smtp_config = self.config['env']
        
        if not smtp_config.get('smtp_username'):
            log.warning("Email not configured, skipping state alert")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_config['smtp_username']
            msg['To'] = smtp_config.get('alert_email', smtp_config['smtp_username'])
            msg['Subject'] = f"🚨 STATE ALERT: {content.get('state')} - {content['headline']}"
            
            body = f"""
STATE-SPECIFIC NEWS DETECTED!

STATE: {content.get('state')}

HEADLINE: {content['headline']}

SUMMARY: {content['summary']}

SUGGESTED FACEBOOK GROUPS:
{chr(10).join(['  • ' + g for g in content.get('suggested_groups', [])])}

This content should be posted to state-specific Facebook groups.

Review via: python main.py state-alerts

---
NDTA News Pipeline
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['smtp_username'], smtp_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            log.info(f"State alert sent for: {content.get('state')}")
            
        except Exception as e:
            log.error(f"Error sending state alert: {e}")

