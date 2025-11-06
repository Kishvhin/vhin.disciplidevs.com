"""
Headline Generator for NDTA Reports
"""
import logging
import openai
from content_generator.prompts import HEADLINE_PROMPT, NDTA_VOICE

log = logging.getLogger(__name__)


class HeadlineGenerator:
    """Generates compelling headlines for NDTA reports"""
    
    def __init__(self, api_key: str):
        openai.api_key = api_key
    
    def generate(self, title: str, summary: str) -> str:
        """Generate a headline"""
        
        prompt = HEADLINE_PROMPT.format(title=title, summary=summary)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": NDTA_VOICE},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            headline = response.choices[0].message.content.strip()
            # Remove quotes if present
            headline = headline.strip('"').strip("'")
            
            return headline
            
        except Exception as e:
            log.error(f"Error generating headline: {e}")
            return title  # Fallback to original

