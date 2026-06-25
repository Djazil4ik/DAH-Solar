# news/views.py
from .models import News, NewsCategory
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


def news(request):
    news_list = News.objects.select_related('category').order_by('-created_at')
    paginator = Paginator(news_list, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'news.html', {'page_obj': page_obj})


def news_category(request, slug):
    news_category = get_object_or_404(NewsCategory, slug=slug)
    news_list = News.objects.filter(category=news_category).select_related(
        'category').order_by('-created_at')
    paginator = Paginator(news_list, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'news_category.html', {
        'page_obj': page_obj,
        'news_category': news_category,
    })


def news_detail(request, slug):
    news_item = get_object_or_404(
        News.objects.select_related('category'), slug=slug)
    previous_news = News.objects.filter(id__lt=news_item.id).order_by('-id').only('slug', 'news_title').first() #type: ignore
    next_news = News.objects.filter(id__gt=news_item.id).order_by('id').only('slug', 'news_title').first() #type: ignore
    return render(request, 'news_detail.html', {
        'news_item': news_item,
        'previous_news': previous_news,
        'next_news': next_news,
    })
