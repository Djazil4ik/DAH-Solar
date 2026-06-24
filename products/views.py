# products/views.py
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from .models import Products, Categories, Type


def _product_qs():
    """Return the base queryset optimized to avoid N+1 query issues"""
    return Products.objects.select_related('category', 'prod_type').order_by('-id')


def products(request):
    page_number = request.GET.get('page', 1)
    cache_key = f'products_page_{page_number}'
    page_obj = cache.get(cache_key)

    if not page_obj:
        paginator = Paginator(_product_qs(), 9)
        page_obj = paginator.get_page(page_number)
        cache.set(cache_key, page_obj, 3600)

    return render(request, 'products/products.html', {'page_obj': page_obj})


def detail_view(request, slug):
    cache_key = f'product_detail_{slug}'
    context = cache.get(cache_key)

    if not context:
        product = get_object_or_404(
            Products.objects.select_related('category', 'prod_type'),
            slug=slug,
        )
        siblings = Products.objects.select_related('category', 'prod_type')

        previous_product = siblings.filter(
            id__lt=product.id).order_by('-id').first() #type: ignore
        next_product = siblings.filter(
            id__gt=product.id).order_by('id').first() #type: ignore

        related_products = list(
            siblings.filter(category=product.category).exclude(
                id=product.id)[:6] #type: ignore
        )

        context = {
            'product': product,
            'previous_product': previous_product,
            'next_product': next_product,
            'related_products': related_products,
        }
        cache.set(cache_key, context, 3600)

    return render(request, 'products/detail_view.html', context)


def category_view(request, slug):
    page_number = request.GET.get('page', 1)
    cache_key = f'category_{slug}_page_{page_number}'
    context = cache.get(cache_key)

    if not context:
        category_page = get_object_or_404(Categories, slug=slug)

        paginator = Paginator(
            _product_qs().filter(category__slug=slug),
            9,
        )
        page_obj = paginator.get_page(page_number)

        context = {'category_page': category_page, 'page_obj': page_obj}
        cache.set(cache_key, context, 3600)

    return render(request, 'products/category.html', context=context)


def type_view(request, category_slug, slug):
    page_number = request.GET.get('page', 1)
    cache_key = f'type_{slug}_page_{page_number}'
    context = cache.get(cache_key)

    if not context:
        category_page = get_object_or_404(Categories, slug=category_slug)
        type_page = get_object_or_404(Type, slug=slug)

        paginator = Paginator(
            _product_qs().filter(prod_type__slug=slug),
            9,
        )
        page_obj = paginator.get_page(page_number)

        context = {
            'category_page': category_page,
            'type_page': type_page,
            'page_obj': page_obj,
        }
        cache.set(cache_key, context, 3600)

    return render(request, 'products/type.html', context=context)
