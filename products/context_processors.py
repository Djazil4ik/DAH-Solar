#products/context_processors.py
from .models import HotProduct, Categories
from .models import Products
from news.models import News, NewsCategory
from projects.models import ProjectCategory
from django.core.cache import cache


def global_site_data(request):
    data = cache.get('global_site_data')
    if not data:
        data = {
            'new_products': list(
                Products.objects
                .select_related('category', 'prod_type', 'brand')
                .order_by('-id')[:4]
            ),
            'first_news': list(
                News.objects
                .select_related('category')
                .only('slug', 'news_title', 'preview', 'created_at', 'category')
                .order_by('-created_at')[:1]
            ),
            'news': list(
                News.objects
                .select_related('category')
                .only('slug', 'news_title', 'preview', 'created_at', 'category')
                .order_by('-created_at')[1:4]
            ),
            'project_categories': list(ProjectCategory.objects.only('slug', 'category_name')),
            'news_categories': list(NewsCategory.objects.only('slug', 'category_name')),
        }
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
    data = cache.get('hot_products')
    if not data:
        data = list(
            HotProduct.objects
            .select_related('product__category', 'product__prod_type', 'product__brand')
        )
        cache.set('hot_products', data, 3600)
    return {'hot_products': data}
