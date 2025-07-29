import json
import urllib.request
from typing import List, Dict
from datetime import datetime

def fetch_aed_waiting_data(lang: str = 'en') -> List[Dict]:
    """Fetch and parse AED waiting time data from Hospital Authority
    
    Args:
        lang: Language code (en/tc/sc) for data format
    
    Returns:
        List of hospital waiting times with hospital_name, waiting_time, update_time
    """
    url = f"https://www.ha.org.hk/opendata/aed/aedwtdata-{lang}.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    # Transform new data format to expected format
    return data

def get_aed_waiting_times(lang: str = 'en') -> Dict:
    """Get current AED waiting times
    
    Args:
        lang: Language code (en/tc/sc) for data format
    """
    data = fetch_aed_waiting_data(lang)
    return {
        'data': data,
        'last_updated': datetime.now().isoformat()
    }
