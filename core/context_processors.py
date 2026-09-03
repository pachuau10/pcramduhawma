from django.templatetags.static import static
from .models import SiteSettings, VisitorCount, NavigationItem


def _absolute(request, url):
    if not url:
        return ''
    if url.startswith(('http://', 'https://')):
        return url
    try:
        return request.build_absolute_uri(url)
    except Exception:
        return url


def site_settings(request):
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None

    try:
        visitor_count = VisitorCount.load()
    except Exception:
        visitor_count = None

    navigation_items = NavigationItem.objects.filter(is_active=True)

    try:
        canonical_url = request.build_absolute_uri(request.path)
    except Exception:
        canonical_url = ''

    default_og_image = ''
    try:
        if settings and settings.og_image:
            default_og_image = _absolute(request, settings.og_image.url)
    except Exception:
        default_og_image = ''
    if not default_og_image:
        try:
            default_og_image = request.build_absolute_uri(static('images/og-image.png'))
        except Exception:
            default_og_image = ''

    return {
        'site_settings': settings,
        'visitor_count': visitor_count,
        'navigation_items': navigation_items,
        'canonical_url': canonical_url,
        'default_og_image': default_og_image,
    }
