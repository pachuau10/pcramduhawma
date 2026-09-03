from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category, Tag


def post_list(request):
    posts = Post.objects.filter(published=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'page_title': 'Blog',
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    posts = Post.objects.filter(published=True)
    post_list_ids = list(posts.values_list('id', flat=True))

    try:
        current_index = post_list_ids.index(post.id)
    except ValueError:
        prev_post = None
        next_post = None
    else:
        prev_post = posts.filter(id__in=post_list_ids[:current_index]).first() if current_index > 0 else None
        next_post = posts.filter(id__in=post_list_ids[current_index + 1:]).first() if current_index < len(post_list_ids) - 1 else None

    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'page_title': post.title,
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    context = {
        'category': category,
        'posts': posts,
        'page_title': f'Category: {category.name}',
    }
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, published=True)
    context = {
        'tag': tag,
        'posts': posts,
        'page_title': f'Tag: {tag.name}',
    }
    return render(request, 'blog/tag_detail.html', context)
