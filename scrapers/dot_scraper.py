"""
DOT Information Scraper for NDTA News Pipeline
Scrapes Department of Transportation news and updates from all 50 states
"""
import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import time

log = logging.getLogger(__name__)


class DOTScraper:
    """Scrape DOT news and updates from state transportation departments"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.dot_config = config.get('dot_sources', {})
        
        # State DOT websites and their news pages
        self.state_dots = self.dot_config.get('state_dots', self._get_default_state_dots())
    
    def _get_default_state_dots(self) -> Dict[str, Dict]:
        """Default state DOT news sources"""
        return {
            'AL': {
                'name': 'Alabama DOT',
                'url': 'https://www.dot.state.al.us/news/',
                'rss': None
            },
            'AK': {
                'name': 'Alaska DOT',
                'url': 'https://dot.alaska.gov/news.shtml',
                'rss': None
            },
            'AZ': {
                'name': 'Arizona DOT',
                'url': 'https://azdot.gov/news',
                'rss': 'https://azdot.gov/news/rss.xml'
            },
            'AR': {
                'name': 'Arkansas DOT',
                'url': 'https://www.ardot.gov/news/',
                'rss': None
            },
            'CA': {
                'name': 'California DOT (Caltrans)',
                'url': 'https://dot.ca.gov/news-releases',
                'rss': 'https://dot.ca.gov/news-releases/rss'
            },
            'CO': {
                'name': 'Colorado DOT',
                'url': 'https://www.codot.gov/news',
                'rss': None
            },
            'CT': {
                'name': 'Connecticut DOT',
                'url': 'https://portal.ct.gov/DOT/News',
                'rss': None
            },
            'DE': {
                'name': 'Delaware DOT',
                'url': 'https://deldot.gov/News/',
                'rss': None
            },
            'FL': {
                'name': 'Florida DOT',
                'url': 'https://www.fdot.gov/info/news.shtm',
                'rss': None
            },
            'GA': {
                'name': 'Georgia DOT',
                'url': 'https://www.dot.ga.gov/news',
                'rss': 'https://www.dot.ga.gov/news/rss'
            },
            'HI': {
                'name': 'Hawaii DOT',
                'url': 'https://hidot.hawaii.gov/highways/news/',
                'rss': None
            },
            'ID': {
                'name': 'Idaho Transportation Department',
                'url': 'https://itd.idaho.gov/news/',
                'rss': None
            },
            'IL': {
                'name': 'Illinois DOT',
                'url': 'https://idot.illinois.gov/about-idot/news-room.html',
                'rss': None
            },
            'IN': {
                'name': 'Indiana DOT',
                'url': 'https://www.in.gov/indot/news/',
                'rss': None
            },
            'IA': {
                'name': 'Iowa DOT',
                'url': 'https://iowadot.gov/news',
                'rss': None
            },
            'KS': {
                'name': 'Kansas DOT',
                'url': 'https://www.ksdot.org/news.asp',
                'rss': None
            },
            'KY': {
                'name': 'Kentucky Transportation Cabinet',
                'url': 'https://transportation.ky.gov/Pages/News.aspx',
                'rss': None
            },
            'LA': {
                'name': 'Louisiana DOTD',
                'url': 'https://wwwsp.dotd.la.gov/Inside_LaDOTD/Pages/News.aspx',
                'rss': None
            },
            'ME': {
                'name': 'Maine DOT',
                'url': 'https://www.maine.gov/mdot/news/',
                'rss': None
            },
            'MD': {
                'name': 'Maryland DOT',
                'url': 'https://www.mdot.maryland.gov/tso/pages/Index.aspx?PageId=24',
                'rss': None
            },
            'MA': {
                'name': 'Massachusetts DOT',
                'url': 'https://www.mass.gov/orgs/massachusetts-department-of-transportation/news',
                'rss': None
            },
            'MI': {
                'name': 'Michigan DOT',
                'url': 'https://www.michigan.gov/mdot/news',
                'rss': None
            },
            'MN': {
                'name': 'Minnesota DOT',
                'url': 'https://www.dot.state.mn.us/newsrels/',
                'rss': None
            },
            'MS': {
                'name': 'Mississippi DOT',
                'url': 'https://mdot.ms.gov/news/',
                'rss': None
            },
            'MO': {
                'name': 'Missouri DOT',
                'url': 'https://www.modot.org/news',
                'rss': None
            },
            'MT': {
                'name': 'Montana DOT',
                'url': 'https://www.mdt.mt.gov/news/',
                'rss': None
            },
            'NE': {
                'name': 'Nebraska DOT',
                'url': 'https://dot.nebraska.gov/news-media/news/',
                'rss': None
            },
            'NV': {
                'name': 'Nevada DOT',
                'url': 'https://www.dot.nv.gov/news',
                'rss': None
            },
            'NH': {
                'name': 'New Hampshire DOT',
                'url': 'https://www.nh.gov/dot/news/',
                'rss': None
            },
            'NJ': {
                'name': 'New Jersey DOT',
                'url': 'https://www.state.nj.us/transportation/about/press/',
                'rss': None
            },
            'NM': {
                'name': 'New Mexico DOT',
                'url': 'https://www.dot.nm.gov/news/',
                'rss': None
            },
            'NY': {
                'name': 'New York DOT',
                'url': 'https://www.dot.ny.gov/news',
                'rss': None
            },
            'NC': {
                'name': 'North Carolina DOT',
                'url': 'https://www.ncdot.gov/news/',
                'rss': None
            },
            'ND': {
                'name': 'North Dakota DOT',
                'url': 'https://www.dot.nd.gov/news/',
                'rss': None
            },
            'OH': {
                'name': 'Ohio DOT',
                'url': 'https://www.transportation.ohio.gov/about-us/news',
                'rss': None
            },
            'OK': {
                'name': 'Oklahoma DOT',
                'url': 'https://oklahoma.gov/odot/news.html',
                'rss': None
            },
            'OR': {
                'name': 'Oregon DOT',
                'url': 'https://www.oregon.gov/odot/Pages/news.aspx',
                'rss': None
            },
            'PA': {
                'name': 'Pennsylvania DOT',
                'url': 'https://www.penndot.pa.gov/pages/all-news.aspx',
                'rss': None
            },
            'RI': {
                'name': 'Rhode Island DOT',
                'url': 'https://www.dot.ri.gov/news/',
                'rss': None
            },
            'SC': {
                'name': 'South Carolina DOT',
                'url': 'https://www.scdot.org/news/',
                'rss': None
            },
            'SD': {
                'name': 'South Dakota DOT',
                'url': 'https://dot.sd.gov/news',
                'rss': None
            },
            'TN': {
                'name': 'Tennessee DOT',
                'url': 'https://www.tn.gov/tdot/news.html',
                'rss': None
            },
            'TX': {
                'name': 'Texas DOT',
                'url': 'https://www.txdot.gov/news.html',
                'rss': None
            },
            'UT': {
                'name': 'Utah DOT',
                'url': 'https://www.udot.utah.gov/connect/news/',
                'rss': None
            },
            'VT': {
                'name': 'Vermont DOT',
                'url': 'https://vtrans.vermont.gov/news',
                'rss': None
            },
            'VA': {
                'name': 'Virginia DOT',
                'url': 'https://www.virginiadot.org/newsroom/',
                'rss': None
            },
            'WA': {
                'name': 'Washington DOT',
                'url': 'https://wsdot.wa.gov/news',
                'rss': None
            },
            'WV': {
                'name': 'West Virginia DOT',
                'url': 'https://transportation.wv.gov/news/Pages/default.aspx',
                'rss': None
            },
            'WI': {
                'name': 'Wisconsin DOT',
                'url': 'https://wisconsindot.gov/Pages/about-wisdot/newsroom/default.aspx',
                'rss': None
            },
            'WY': {
                'name': 'Wyoming DOT',
                'url': 'https://www.dot.state.wy.us/news',
                'rss': None
            }
        }
    
    def scrape_state_dot(self, state_code: str, lookback_days: int = 7) -> List[Dict]:
        """Scrape news from a specific state DOT"""
        articles = []
        
        if state_code not in self.state_dots:
            log.warning(f"No DOT configuration for state: {state_code}")
            return articles
        
        dot_info = self.state_dots[state_code]
        
        try:
            log.info(f"Scraping {dot_info['name']}...")
            
            # Try RSS first if available
            if dot_info.get('rss'):
                articles = self._scrape_rss(state_code, dot_info, lookback_days)
            
            # If no RSS or RSS failed, try web scraping
            if not articles:
                articles = self._scrape_web(state_code, dot_info, lookback_days)
            
            log.info(f"  ✓ Found {len(articles)} articles from {dot_info['name']}")
            
        except Exception as e:
            log.error(f"Error scraping {dot_info['name']}: {e}")
        
        return articles
    
    def _scrape_rss(self, state_code: str, dot_info: Dict, lookback_days: int) -> List[Dict]:
        """Scrape DOT news from RSS feed"""
        # This would use the RSS scraper - placeholder for now
        return []
    
    def _scrape_web(self, state_code: str, dot_info: Dict, lookback_days: int) -> List[Dict]:
        """Scrape DOT news from website"""
        articles = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(dot_info['url'], headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Generic news article detection (this is a simplified version)
                # Each state DOT has different HTML structure, so this is a best-effort approach
                news_items = soup.find_all(['article', 'div'], class_=lambda x: x and ('news' in x.lower() or 'press' in x.lower()))
                
                for item in news_items[:10]:  # Limit to 10 most recent
                    try:
                        title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'a'])
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        # Try to find link
                        link_elem = item.find('a', href=True)
                        url = link_elem['href'] if link_elem else dot_info['url']
                        if url.startswith('/'):
                            # Make absolute URL
                            base_url = '/'.join(dot_info['url'].split('/')[:3])
                            url = base_url + url
                        
                        # Try to find description
                        desc_elem = item.find('p')
                        description = desc_elem.get_text(strip=True) if desc_elem else title
                        
                        # Check if state-specific (priority states)
                        priority_states = ['GA', 'FL', 'AL', 'SC', 'NC', 'TN', 'TX', 'CA']
                        is_state_specific = state_code in priority_states

                        article = {
                            'id': f"{state_code}_{hash(url) % 1000000}",
                            'title': title,
                            'description': description[:500],
                            'url': url,
                            'source': dot_info['name'],
                            'published_date': datetime.now().isoformat(),  # Actual date parsing would be state-specific
                            'state': state_code,
                            'category': 'DOT_News',
                            'is_relevant': True,  # DOT news is pre-filtered
                            'relevance_score': 8.0 if is_state_specific else 6.0,
                            'is_state_specific': is_state_specific,
                            'status': 'pending_review',
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        articles.append(article)
                        
                    except Exception as e:
                        log.debug(f"Error parsing news item: {e}")
                        continue
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            log.error(f"Error scraping {dot_info['name']} website: {e}")
        
        return articles
    
    def scrape_all_states(self, lookback_days: int = 7, priority_states: List[str] = None) -> List[Dict]:
        """Scrape DOT news from all states or priority states"""
        all_articles = []
        
        # If priority states specified, scrape those first
        states_to_scrape = priority_states if priority_states else list(self.state_dots.keys())
        
        log.info(f"Starting DOT scrape for {len(states_to_scrape)} states")
        
        for state_code in states_to_scrape:
            articles = self.scrape_state_dot(state_code, lookback_days)
            all_articles.extend(articles)
        
        log.info(f"DOT scrape complete: {len(all_articles)} total articles")
        
        return all_articles

