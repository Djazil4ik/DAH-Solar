from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from products.models import Products, Categories, Type, Second_Category
from projects.models import Project, ProjectCategory
from news.models import News, NewsCategory
from videoapp.models import Video

def home(request):
    # Используем .filter().first(), чтобы сайт не падал при пустой БД
    category_solar_system = Second_Category.objects.filter(id=1).first()
    category_pv_module = Categories.objects.filter(category="PV Module").first()
    
    # Фильтруем модули, если категория существует
    pv_modules = Products.objects.filter(category=category_pv_module).order_by('-id')[:6] if category_pv_module else []
    
    # Новости по категориям (используем filter().first() для безопасности)
    global_exhibitions = NewsCategory.objects.filter(id=1).first()
    events = NewsCategory.objects.filter(id=2).first()
    social_activities = NewsCategory.objects.filter(id=3).first()

    context = {
        "pv_modules": pv_modules,
        "solar_systems": Products.objects.filter(second_category__second_category="Solar Unit")[:6],
        "projects": Project.objects.all().order_by('id')[:6],
        "news_global_exhibitions": News.objects.filter(category=global_exhibitions).order_by('id')[:6] if global_exhibitions else [],
        "news_events": News.objects.filter(category=events).order_by('id')[:6] if events else [],
        "news_social_activities": News.objects.filter(category=social_activities).order_by('id')[:6] if social_activities else [],
        "videos": Video.objects.order_by('-id')[:3]
    }
    return render(request, 'main/home.html', context)


def products(request):
    products_all = Products.objects.all().order_by('-id')
    paginator = Paginator(products_all, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'products/products.html', {'page_obj': page_obj})


def detail_view(request, slug):
    product = get_object_or_404(Products, slug=slug)
    
    context = {
        'product': product,
        'previous_product': Products.objects.filter(id__lt=product.id).order_by('-id').first(), #type: ignore
        'next_product': Products.objects.filter(id__gt=product.id).order_by('id').first(), #type: ignore
        'related_products': Products.objects.filter(category=product.category).exclude(id=product.id)[:6], #type: ignore
    }
    return render(request, 'products/detail_view.html', context)


def category_view(request, slug):
    category_page = get_object_or_404(Categories, slug=slug)
    products_list = Products.objects.filter(category__slug=slug).order_by('-id')
    
    paginator = Paginator(products_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'products/category.html', {
        'category_page': category_page, 
        'page_obj': page_obj
    })


def type_view(request, category_slug, slug):
    category_page = get_object_or_404(Categories, slug=category_slug)
    type_page = get_object_or_404(Type, slug=slug)
    products_list = Products.objects.filter(prod_type__slug=slug).order_by('-id')
    
    paginator = Paginator(products_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'products/type.html', {
        'category_page': category_page,
        'type_page': type_page,
        'page_obj': page_obj
    })


def search_results(request):
    query = request.GET.get("query")
    results = Products.objects.filter(prod_model__icontains=query) if query else None
    
    return render(request, "main/search_results.html", {
        "results": results,
        "query": query
    })