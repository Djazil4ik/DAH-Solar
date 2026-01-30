from django.shortcuts import render
from products.models import Products
from news.models import News, NewsCategory
from projects.models import ProjectCategory


def dahsolar(request):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()

    context = {
        'new_products': new_products,
        'first_news': first_news,
        'news': news,
        'project_categories': project_categories,
        'news_categories': news_categories,
    }
    return render(request, 'dahsolar/dahsolar.html', context=context)


def overview(request):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()

    context = {
        'new_products': new_products,
        'first_news': first_news,
        'news': news,
        'project_categories': project_categories,
        'news_categories': news_categories,
    }
    return render(request, 'dahsolar/overview.html', context=context)


def dah_factories(request):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()

    context = {
        'new_products': new_products,
        'first_news': first_news,
        'news': news,
        'project_categories': project_categories,
        'news_categories': news_categories,
    }
    return render(request, 'dahsolar/dah-factories.html', context=context)

def vission_mission(request):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()

    context = {
        'new_products': new_products,
        'first_news': first_news,
        'news': news,
        'project_categories': project_categories,
        'news_categories': news_categories,
    }
    return render(request, 'dahsolar/vission-mission.html', context=context)