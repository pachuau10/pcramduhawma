from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    projects = Project.objects.filter(published=True)
    featured = projects.filter(featured=True)
    context = {
        'projects': projects,
        'featured': featured,
        'page_title': 'Projects',
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, published=True)
    context = {
        'project': project,
        'page_title': project.name,
    }
    return render(request, 'projects/project_detail.html', context)
