"""
State-Specific News Detector
"""
import logging
import re
from typing import Dict, List

log = logging.getLogger(__name__)


class StateDetector:
    """Detects state-specific news and suggests Facebook groups"""
    
    def __init__(self):
        self.states = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
            'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
            'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
            'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
            'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
            'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
            'WI': 'Wisconsin', 'WY': 'Wyoming'
        }
        
        # Facebook group mapping (you'll customize this)
        self.facebook_groups = {
            'GA': ['Georgia Dump Truck Operators', 'GA Heavy Equipment Network'],
            'TX': ['Texas Dump Truck Association', 'TX Trucking Professionals'],
            'CA': ['California Dump Truck Owners', 'CA Heavy Haulers'],
            'FL': ['Florida Dump Truck Network', 'FL Construction Trucking'],
            # Add more as needed
        }
    
    def detect(self, text: str) -> Dict:
        """Detect states mentioned in text"""
        
        text_lower = text.lower()
        detected = []
        
        for abbr, name in self.states.items():
            # Check for state name or abbreviation
            if name.lower() in text_lower or f" {abbr.lower()} " in text_lower:
                detected.append({
                    'abbr': abbr,
                    'name': name,
                    'suggested_groups': self.facebook_groups.get(abbr, [])
                })
        
        return {
            'is_state_specific': len(detected) > 0,
            'states': detected,
            'confidence': 0.9 if detected else 0.0
        }
    
    def get_facebook_groups(self, state_abbr: str) -> List[str]:
        """Get Facebook groups for a state"""
        return self.facebook_groups.get(state_abbr, [])

