from django.shortcuts import render
from .utils import get_cached_data

def dashboard(request):
    context = {
        "cisa_data": get_cached_data("cisa_kev"),
        "mitre_data": get_cached_data("mitre_attack"),
    }
    return render(request, "threat_feeds/dashboard.html", context)
