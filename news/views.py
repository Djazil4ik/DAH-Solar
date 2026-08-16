# news/views.py
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language

from .models import News, NewsCategory, NewsImage


def news(request):
    lang = get_language()
    page = request.GET.get('page', 1)
    cache_key = f'news_list_{page}_{lang}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    news_list = News.objects.select_related('category').prefetch_related(
        Prefetch('images', queryset=NewsImage.objects.order_by('id'))
    ).order_by('-created_at')

    paginator = Paginator(news_list, 6)
    page_obj = paginator.get_page(page)

    response = render(request, 'news.html', {'page_obj': page_obj})
    cache.set(cache_key, response, 3600)
    return response


def news_category(request, slug):
    lang = get_language()
    page = request.GET.get('page', 1)
    cache_key = f'news_category_{slug}_{page}_{lang}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    news_category = get_object_or_404(NewsCategory, slug=slug)
    news_list = News.objects.filter(category=news_category).select_related('category').prefetch_related(
        Prefetch('images', queryset=NewsImage.objects.order_by('id'))
    ).order_by('-created_at')

    paginator = Paginator(news_list, 6)
    page_obj = paginator.get_page(page)

    response = render(request, 'news_category.html', {
        'page_obj': page_obj,
        'news_category': news_category,
    })
    cache.set(cache_key, response, 3600)
    return response


def news_detail(request, slug):
    lang = get_language()
    cache_key = f'news_detail_{slug}_{lang}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    news_item = get_object_or_404(
        News.objects.select_related('category').prefetch_related(
            Prefetch('images', queryset=NewsImage.objects.order_by('id'))
        ),
        slug=slug,
    )

    # Previous/next articles for in-page navigation
    previous_news = News.objects.filter(id__lt=news_item.id).order_by(
        '-id').only('slug', 'news_title').first()
    next_news = News.objects.filter(id__gt=news_item.id).order_by(
        'id').only('slug', 'news_title').first()

    response = render(request, 'news_detail.html', {
        'news_item': news_item,
        'previous_news': previous_news,
        'next_news': next_news,
    })
    cache.set(cache_key, response, 3600)
    return response
