from django import template

register = template.Library()


@register.filter
def absurl(url, request):
    if not url:
        return ''
    if url.startswith(('http://', 'https://')):
        return url
    try:
        return request.build_absolute_uri(url)
    except Exception:
        return url
