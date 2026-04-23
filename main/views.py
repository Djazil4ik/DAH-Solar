# main/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from products.models import Products, Categories, Type
from projects.models import Project
from news.models import News, NewsCategory
from videoapp.models import Video

def home(request):
    # Используем .filter().first(), чтобы сайт не падал при пустой БД
    category_solar_system = Categories.objects.filter(
        slug="solarunit-system").first()
    category_pv_module = Categories.objects.filter(slug="pv-module").first()
    

    # Фильтруем модули, если категория существует
    pv_modules = Products.objects.filter(category=category_pv_module).prefetch_related('products_images').order_by('-id')[:6] if category_pv_module else []
    solar_systems = Products.objects.filter(category=category_solar_system).prefetch_related('products_images').order_by('-id')[:6] if category_solar_system else []

    # Новости по категориям (используем filter().first() для безопасности)
    global_exhibitions = NewsCategory.objects.filter(slug="global-exhibitions").first()
    events = NewsCategory.objects.filter(slug="events").first()
    social_activities = NewsCategory.objects.filter(slug="social-activities").first()

    context = {
        "pv_modules": pv_modules,
        "solar_systems": solar_systems,
        "projects": Project.objects.all().order_by('id')[:6],
        "news_global_exhibitions": News.objects.filter(category=global_exhibitions).order_by('id')[:6] if global_exhibitions else [],
        "news_events": News.objects.filter(category=events).order_by('id')[:6] if events else [],
        "news_social_activities": News.objects.filter(category=social_activities).order_by('id')[:6] if social_activities else [],
        "videos": Video.objects.order_by('-id')[:3]
    }
    return render(request, 'main/home.html', context)


def search_results(request):
    query = request.GET.get("query")
    results = Products.objects.filter(prod_model__icontains=query) if query else None
    
    return render(request, "main/search_results.html", {
        "results": results,
        "query": query
    })