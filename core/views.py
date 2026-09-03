from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from .models import SiteSettings, NavigationItem, Link
from blog.models import Post
from software.models import Software
from projects.models import Project
from gallery.models import GalleryImage
from guestbook.models import GuestbookEntry


def home(request):
    settings = SiteSettings.load()
    latest_posts = Post.objects.filter(published=True)[:3]
    latest_software = Software.objects.filter(published=True).order_by('-release_date')[:3]
    latest_projects = Project.objects.filter(published=True)[:3]
    working_on_projects = Project.objects.filter(published=True, status='active')[:3]
    recent_guestbook = GuestbookEntry.objects.filter(is_approved=True)[:3]
    context = {
        'settings': settings,
        'latest_posts': latest_posts,
        'latest_software': latest_software,
        'latest_projects': latest_projects,
        'working_on_projects': working_on_projects,
        'recent_guestbook': recent_guestbook,
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)


def about(request):
    settings = SiteSettings.load()
    context = {
        'settings': settings,
        'page_title': 'About Me',
    }
    return render(request, 'about.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    results = {
        'posts': [],
        'software': [],
        'projects': [],
    }
    if query:
        results['posts'] = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query),
            published=True
        )
        results['software'] = Software.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            published=True
        )
        results['projects'] = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            published=True
        )
    context = {
        'query': query,
        'results': results,
        'total_results': sum(len(v) for v in results.values()),
        'page_title': f'Search: {query}' if query else 'Search',
    }
    return render(request, 'search/results.html', context)


def contact(request):
    from django.contrib import messages
    from .forms import ContactForm
    settings = SiteSettings.load()
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = request.META.get('REMOTE_ADDR')
            msg.save()
            messages.success(request, 'Thanks! Your message has been received.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {
        'settings': settings,
        'form': form,
        'page_title': 'Contact',
    }
    return render(request, 'contact.html', context)


def robots_txt(request):
    from django.http import HttpResponse
    content = "User-agent: *\nDisallow: /admin/\nSitemap: /sitemap.xml\n"
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    from django.http import HttpResponse
    from django.utils import timezone
    base_url = request.build_absolute_uri('/')

    urls = [
        {'loc': base_url, 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '1.0'},
        {'loc': f'{base_url}about/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.8'},
        {'loc': f'{base_url}blog/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.9'},
        {'loc': f'{base_url}software/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.9'},
        {'loc': f'{base_url}projects/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.8'},
        {'loc': f'{base_url}gallery/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.7'},
        {'loc': f'{base_url}guestbook/', 'lastmod': timezone.now().strftime('%Y-%m-%d'), 'priority': '0.6'},
    ]

    for post in Post.objects.filter(published=True):
        urls.append({
            'loc': f'{base_url}blog/{post.slug}/',
            'lastmod': post.updated_at.strftime('%Y-%m-%d'),
            'priority': '0.7',
        })

    for sw in Software.objects.filter(published=True):
        urls.append({
            'loc': f'{base_url}software/{sw.slug}/',
            'lastmod': sw.updated_at.strftime('%Y-%m-%d'),
            'priority': '0.8',
        })

    for project in Project.objects.filter(published=True):
        urls.append({
            'loc': f'{base_url}projects/{project.slug}/',
            'lastmod': project.updated_at.strftime('%Y-%m-%d'),
            'priority': '0.7',
        })

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url>\n    <loc>{url["loc"]}</loc>\n    <lastmod>{url["lastmod"]}</lastmod>\n    <priority>{url["priority"]}</priority>\n  </url>\n'
    xml += '</urlset>'

    return HttpResponse(xml, content_type='application/xml')
