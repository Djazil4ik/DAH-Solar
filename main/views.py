# main/views.py
from django.db.models import Prefetch
from django.shortcuts import render

from news.models import News, NewsCategory
from products.models import Categories, Products
from projects.models import Project


def home(request):
    # Use .filter().first() so the site doesn't break on an empty DB
    category_solar_system = Categories.objects.filter(
        slug="solarunit-system").first()
    category_pv_module = Categories.objects.filter(slug="pv-module").first()

    # Only query products if the corresponding category exists
    pv_modules = (
        Products.objects.filter(category=category_pv_module)
        .prefetch_related('products_images')
        .order_by('-id')[:6]
        if category_pv_module
        else []
    )
    solar_systems = (
        Products.objects.filter(category=category_solar_system)
        .prefetch_related('products_images')
        .order_by('-id')[:6]
        if category_solar_system
        else []
    )

    # Latest news, grouped by category
    news_queryset = News.objects.order_by(
        '-created_at').prefetch_related('images')[:6]

    news_categories = NewsCategory.objects.prefetch_related(
        Prefetch('news', queryset=news_queryset, to_attr='limited_news')
    )

    context = {
        "pv_modules": pv_modules,
        "solar_systems": solar_systems,
        "projects": Project.objects.all().order_by('id')[:6],
        # Categories already carry their limited news via limited_news
        "news_categories": news_categories,
    }
    return render(request, 'main/home.html', context)


def search_results(request):
    query = request.GET.get("query")
    results = Products.objects.filter(
        prod_model__icontains=query) if query else None

    return render(request, "main/search_results.html", {
        "results": results,
        "query": query,
    })
