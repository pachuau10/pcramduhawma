from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import Software


def software_list(request):
    software_items = Software.objects.filter(published=True)
    featured = software_items.filter(featured=True)
    context = {
        'software_items': software_items,
        'featured': featured,
        'page_title': 'Software Downloads',
    }
    return render(request, 'software/software_list.html', context)


def software_detail(request, slug):
    sw = get_object_or_404(Software, slug=slug, published=True)
    context = {
        'software': sw,
        'page_title': sw.name,
    }
    return render(request, 'software/software_detail.html', context)


def software_download(request, slug):
    sw = get_object_or_404(Software, slug=slug, published=True)

    if not sw.file:
        raise Http404("File not found.")

    sw.increment_download()

    try:
        response = FileResponse(sw.file.open('rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{sw.file.name.split("/")[-1]}"'
        return response
    except FileNotFoundError:
        raise Http404("File not found on server.")
