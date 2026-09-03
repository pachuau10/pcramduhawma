from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import GalleryImage


def gallery_list(request):
    images = GalleryImage.objects.all()
    context = {
        'images': images,
        'page_title': 'Gallery',
    }
    return render(request, 'gallery/gallery_list.html', context)


def gallery_detail(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'title': image.title,
            'description': image.description,
            'image_url': image.image.url if image.image else '',
        })
    context = {
        'image': image,
        'page_title': image.title,
    }
    return render(request, 'gallery/gallery_detail.html', context)
