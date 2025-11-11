from django.conf import settings

def static_url(request):
    """Context processor to make STATIC_URL available in all templates"""
    return {'STATIC_URL': settings.STATIC_URL}

