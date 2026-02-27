from .models import HotProduct, Categories
from .models import Products
from news.models import News, NewsCategory
from projects.models import ProjectCategory
from django.core.cache import cache


def global_site_data(request):
    # Пытаемся достать всё разом из кэша
    data = cache.get('global_site_data')
    if not data:
        data = {
            'new_products': list(Products.objects.order_by('-id')[:4]),
            'first_news': list(News.objects.order_by('-id')[:1]),
            'news': list(News.objects.order_by('-id')[1:4]),
            'project_categories': list(ProjectCategory.objects.all()),
            'news_categories': list(NewsCategory.objects.all()),
        }
        # Кэшируем на 1 час (3600 сек)
        cache.set('global_site_data', data, 3600)
    return data


def categories_processor(request):
    # Категории в меню меняются еще реже
    cats = cache.get('navbar_categories')
    if not cats:
        cats = list(Categories.objects.prefetch_related('types').all())
        cache.set('navbar_categories', cats, 86400)  # На сутки
    return {'navbar_categories': cats}

def hot_products(request):
    hot_products = HotProduct.objects.select_related('product')
    return {'hot_products': hot_products}
