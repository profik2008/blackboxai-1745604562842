import requests
from django.utils import timezone
from .models import CachedAPIData
from datetime import timedelta

def fetch_cisa_kev():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("vulnerabilities", [])[:10]  # Get first 10
    except Exception:
        return []

def fetch_mitre_attack():
    url = "https://attack.mitre.org/api/v2/techniques/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("techniques", [])[:10]  # Get first 10
    except Exception:
        return []

def get_cached_data(api_name):
    # Check if cached data exists and is recent (<1 hour old)
    try:
        cached = CachedAPIData.objects.get(api_name=api_name)
        if cached.last_updated > timezone.now() - timedelta(hours=1):
            return cached.data
    except CachedAPIData.DoesNotExist:
        pass
    
    # Fetch fresh data
    if api_name == "cisa_kev":
        new_data = fetch_cisa_kev()
    elif api_name == "mitre_attack":
        new_data = fetch_mitre_attack()
    else:
        return None

    # Update cache
    CachedAPIData.objects.update_or_create(
        api_name=api_name,
        defaults={"data": new_data}
    )
    return new_data
