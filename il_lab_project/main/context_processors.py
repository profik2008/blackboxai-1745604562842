from django.conf import settings

def company_info(request):
    return {
        'company_phone': settings.COMPANY_PHONE
    }
