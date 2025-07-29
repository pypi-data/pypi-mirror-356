import json
import urllib.request
from typing import List, Dict
from datetime import datetime

def fetch_specialist_waiting_data(lang: str = 'en') -> List[Dict]:
    """Fetch and parse specialist outpatient waiting time data from Hospital Authority
    
    Args:
        lang: Language code (en/tc/sc) for data format
    
    Returns:
        List of specialist waiting times with cluster, specialty, category, description, and value
    """
    url = f"https://www.ha.org.hk/opendata/sop/sop-waiting-time-{lang}.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    return data

def get_specialist_waiting_times(lang: str = 'en') -> Dict:
    """Get current waiting times for new case bookings for specialist outpatient services
    
    Args:
        lang: Language code (en/tc/sc) for data format
    """
    data = fetch_specialist_waiting_data(lang)
    return {
        'data': data,
        'last_updated': datetime.now().isoformat()
    }
