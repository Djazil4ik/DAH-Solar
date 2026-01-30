from django.shortcuts import render
from products.models import Products, Categories, Second_Category
from projects.models import Project, ProjectCategory
from news.models import News, NewsCategory
from videoapp.models import Video


def home(request):
    category_solar_system = Second_Category.objects.get(
        id=1)  # id=1 это категория Solar Unit
    category_pv_module = Categories.objects.get(
        id=1)  # id=1 это категория PV_Modules
    pv_modules = Products.objects.filter(
        category=category_pv_module).order_by('-id')[:6]
    solar_systems = solar_systems = Products.objects.filter(second_category__second_category="Solar Unit")[:6]

    projects = Project.objects.all().order_by('id')[:6]
    project_categories = ProjectCategory.objects.all()
    global_exhibitions = NewsCategory.objects.get(
        id=1)  # id=1 это категория Global Exhibitions
    events = NewsCategory.objects.get(id=2)  # id=2 это категория Events
    social_activities = NewsCategory.objects.get(
        id=3)  # id=3 это категория Social Activities
    news_global_exhibitions = News.objects.filter(
        category=global_exhibitions).order_by('id')[:6]
    news_events = News.objects.filter(category=events).order_by('id')[:6]
    news_social_activities = News.objects.filter(
        category=social_activities).order_by('id')[:6]
    news_categories = NewsCategory.objects.all()
    videos = Video.objects.order_by('-id')[:3]
    context = {
        "pv_modules": pv_modules,
        "solar_systems": solar_systems,
        "projects": projects,
        "project_categories": project_categories,
        "news_global_exhibitions": news_global_exhibitions,
        "news_events": news_events,
        "news_social_activities": news_social_activities,
        "news_categories": news_categories,
        "videos": videos
    }

    return render(request, 'main/home.html', context=context)


def search_results(request):
    query = request.GET.get("query")
    results = Products.objects.filter(
        prod_model__icontains=query) if query else None
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    news_categories = NewsCategory.objects.all()
    project_categories = ProjectCategory.objects.all()
    context = {
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        "results": results,
        "news_categories": news_categories,
        "project_categories": project_categories,
        "query": query
    }
    return render(request, "main/search_results.html", context=context)
