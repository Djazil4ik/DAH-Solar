from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from .models import Products, Categories, Type
from news.models import News, NewsCategory
from projects.models import ProjectCategory


def products(request):
    products_list = Products.objects.all().order_by('-id')
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/products.html', {'page_obj': page_obj})


def detail_view(request, slug):
    # Создаем уникальный ключ для каждого товара
    cache_key = f'product_detail_{slug}'
    context = cache.get(cache_key)

    if not context:
        product = get_object_or_404(Products, slug=slug)
        previous_product = Products.objects.filter(
            id__lt=product.id).order_by('-id').first() #type: ignore
        next_product = Products.objects.filter(
            id__gt=product.id).order_by('id').first() #type: ignore
        related_products = list(Products.objects.filter(
            category=product.category).exclude(id=product.id)[:6]) #type: ignore

        context = {
            'product': product,
            'previous_product': previous_product,
            'next_product': next_product,
            'related_products': related_products,
        }
        cache.set(cache_key, context, 3600)

    return render(request, 'products/detail_view.html', context)


def category_view(request, slug):
    category_page  = get_object_or_404(Categories, slug=slug)
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    products = Products.objects.filter(category__slug=slug)
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()  # Получаем все категории проектов
    context = {
        'category_page': category_page,
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        'page_obj': page_obj,
        'project_categories': project_categories,
        "news_categories": news_categories,
    }

    return render(request, 'products/category.html', context=context)

def type_view(request, category_slug, slug):
    category_page = get_object_or_404(Categories, slug=category_slug)
    type_page = get_object_or_404(Type, slug=slug)
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    products = Products.objects.filter(prod_type__slug=slug)
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()  # Получаем все категории проектов
    context = {
        'category_page': category_page,
        'type_page': type_page,
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        'page_obj': page_obj,
        'project_categories': project_categories,
        "news_categories": news_categories,
    }

    return render(request, 'products/type.html', context=context)