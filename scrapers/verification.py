"""
Article Verification and Quality Checks
Ensures scraped news is legitimate, accurate, and from trusted sources
"""
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import openai
from urllib.parse import urlparse

log = logging.getLogger(__name__)


class ArticleVerifier:
    """Verify article legitimacy and quality"""
    
    # Trusted news sources for construction/trucking industry
    TRUSTED_SOURCES = {
        'enr.com': {'name': 'Engineering News-Record', 'trust_score': 10},
        'constructiondive.com': {'name': 'Construction Dive', 'trust_score': 10},
        'equipmentworld.com': {'name': 'Equipment World', 'trust_score': 9},
        'forconstructionpros.com': {'name': 'For Construction Pros', 'trust_score': 9},
        'constructionequipment.com': {'name': 'Construction Equipment', 'trust_score': 9},
        'truckinginfo.com': {'name': 'Trucking Info', 'trust_score': 9},
        'fleetowner.com': {'name': 'Fleet Owner', 'trust_score': 9},
        'overdriveonline.com': {'name': 'Overdrive', 'trust_score': 8},
        'ccjdigital.com': {'name': 'Commercial Carrier Journal', 'trust_score': 9},
        'constructiondive.com': {'name': 'Construction Dive', 'trust_score': 10},
        'reuters.com': {'name': 'Reuters', 'trust_score': 10},
        'apnews.com': {'name': 'Associated Press', 'trust_score': 10},
        'bloomberg.com': {'name': 'Bloomberg', 'trust_score': 9},
        'wsj.com': {'name': 'Wall Street Journal', 'trust_score': 9},
    }
    
    # Red flags in content
    RED_FLAGS = [
        'click here now',
        'limited time offer',
        'act now',
        'you won\'t believe',
        'shocking',
        'miracle',
        'secret',
        'doctors hate',
        'one weird trick',
    ]
    
    def __init__(self, config: Dict):
        self.config = config
        api_key = config['env'].get('openai_api_key')
        if api_key:
            openai.api_key = api_key
    
    def verify_source(self, article: Dict) -> Dict:
        """Verify the source is legitimate and trusted"""
        url = article.get('url', '')
        domain = urlparse(url).netloc.lower()
        
        # Remove www. prefix
        domain = domain.replace('www.', '')
        
        # Check if source is in trusted list
        trust_info = None
        for trusted_domain, info in self.TRUSTED_SOURCES.items():
            if trusted_domain in domain:
                trust_info = info
                break
        
        if trust_info:
            return {
                'is_trusted': True,
                'trust_score': trust_info['trust_score'],
                'source_name': trust_info['name'],
                'verification': 'Verified trusted source'
            }
        else:
            return {
                'is_trusted': False,
                'trust_score': 5,
                'source_name': domain,
                'verification': 'Unknown source - requires manual verification'
            }
    
    def check_content_quality(self, article: Dict) -> Dict:
        """Check for red flags and quality issues"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        content = f"{title} {summary}"
        
        # Check for red flags
        flags_found = []
        for flag in self.RED_FLAGS:
            if flag in content:
                flags_found.append(flag)
        
        # Check article age
        pub_date = article.get('published_date')
        is_recent = True
        age_days = None
        
        if pub_date:
            try:
                if isinstance(pub_date, str):
                    pub_datetime = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                else:
                    pub_datetime = pub_date
                
                age = datetime.now(pub_datetime.tzinfo) - pub_datetime
                age_days = age.days
                is_recent = age_days <= 30  # Consider articles up to 30 days old
            except:
                pass
        
        # Check for minimum content length
        has_sufficient_content = len(summary) >= 100
        
        # Check for required fields
        has_required_fields = all([
            article.get('title'),
            article.get('url'),
            article.get('summary'),
            article.get('source')
        ])
        
        quality_score = 10
        issues = []
        
        if flags_found:
            quality_score -= len(flags_found) * 2
            issues.append(f"Red flags found: {', '.join(flags_found)}")
        
        if not is_recent:
            quality_score -= 2
            issues.append(f"Article is {age_days} days old")
        
        if not has_sufficient_content:
            quality_score -= 3
            issues.append("Insufficient content length")
        
        if not has_required_fields:
            quality_score -= 5
            issues.append("Missing required fields")
        
        return {
            'quality_score': max(0, quality_score),
            'red_flags': flags_found,
            'is_recent': is_recent,
            'age_days': age_days,
            'has_sufficient_content': has_sufficient_content,
            'has_required_fields': has_required_fields,
            'issues': issues
        }
    
    def verify_facts_with_ai(self, article: Dict) -> Dict:
        """Use AI to verify factual accuracy and detect misinformation"""
        
        prompt = f"""You are a fact-checking expert for construction and trucking industry news.

Analyze this article for:
1. Factual accuracy - Does it make verifiable claims?
2. Credibility - Does it cite sources or provide evidence?
3. Bias detection - Is it objective or promotional?
4. Misinformation risk - Any signs of false or misleading information?

Article:
Title: {article['title']}
Source: {article.get('source', 'Unknown')}
Summary: {article['summary'][:800]}

Respond in JSON format:
{{
    "appears_factual": true/false,
    "credibility_score": 1-10,
    "has_citations": true/false,
    "bias_level": "low/medium/high",
    "misinformation_risk": "low/medium/high",
    "concerns": ["list any concerns"],
    "recommendation": "approve/review/reject"
}}"""
        
        try:
            time.sleep(1)  # Rate limiting
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Lower temperature for more consistent fact-checking
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            log.error(f"Error in AI fact-checking: {e}")
            return {
                "appears_factual": True,
                "credibility_score": 5,
                "has_citations": False,
                "bias_level": "unknown",
                "misinformation_risk": "unknown",
                "concerns": ["AI verification failed"],
                "recommendation": "review"
            }
    
    def comprehensive_verification(self, article: Dict) -> Dict:
        """Run all verification checks and return comprehensive results"""
        
        log.info(f"Verifying article: {article.get('title', 'Unknown')}")
        
        # 1. Source verification
        source_check = self.verify_source(article)
        
        # 2. Content quality check
        quality_check = self.check_content_quality(article)
        
        # 3. AI fact-checking (only for trusted sources to save API calls)
        if source_check['is_trusted']:
            fact_check = self.verify_facts_with_ai(article)
        else:
            fact_check = {
                "appears_factual": False,
                "credibility_score": 3,
                "recommendation": "review",
                "concerns": ["Untrusted source - manual verification required"]
            }
        
        # Calculate overall verification score
        overall_score = (
            source_check['trust_score'] * 0.4 +
            quality_check['quality_score'] * 0.3 +
            fact_check['credibility_score'] * 0.3
        )
        
        # Determine final recommendation
        if overall_score >= 8 and source_check['is_trusted'] and fact_check.get('recommendation') == 'approve':
            final_recommendation = 'auto_approve'
        elif overall_score >= 6:
            final_recommendation = 'manual_review'
        else:
            final_recommendation = 'reject'
        
        # Compile all verification data
        verification_result = {
            'verified_at': datetime.now().isoformat(),
            'overall_score': round(overall_score, 2),
            'recommendation': final_recommendation,
            'source_verification': source_check,
            'quality_check': quality_check,
            'fact_check': fact_check,
            'verification_passed': overall_score >= 6
        }
        
        # Add verification to article
        article['verification'] = verification_result
        
        log.info(f"Verification complete - Score: {overall_score:.2f}, Recommendation: {final_recommendation}")
        
        return verification_result
    
    def get_verification_summary(self, article: Dict) -> str:
        """Get human-readable verification summary"""
        verification = article.get('verification', {})
        
        if not verification:
            return "Not verified"
        
        score = verification.get('overall_score', 0)
        recommendation = verification.get('recommendation', 'unknown')
        source = verification.get('source_verification', {})
        
        summary = f"✓ Verification Score: {score}/10\n"
        summary += f"✓ Source: {source.get('source_name', 'Unknown')} "
        
        if source.get('is_trusted'):
            summary += f"(Trusted - {source.get('trust_score')}/10)\n"
        else:
            summary += "(Unverified source)\n"
        
        summary += f"✓ Recommendation: {recommendation.upper()}\n"
        
        concerns = verification.get('fact_check', {}).get('concerns', [])
        if concerns:
            summary += f"⚠️  Concerns: {', '.join(concerns)}\n"
        
        return summary

