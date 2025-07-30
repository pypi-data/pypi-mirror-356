import requests
from requests.adapters import HTTPAdapter, Retry
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

def is_on_pypi(package: str) -> bool:
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        response = session.get(
            url,
            timeout=5,
            headers={'User-Agent': 'slopsquat-detector/1.0'}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
