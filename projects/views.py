from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory
from products.models import Products
from news.models import News, NewsCategory
from django.core.paginator import Paginator


def projects(request):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    projects = Project.objects.all()
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()
    paginator = Paginator(projects, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        'project_categories': project_categories,
        "news_categories": news_categories,
        'page_obj': page_obj
    }
    return render(request, 'projects.html', context=context)


def detail_view(request, slug):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    project = get_object_or_404(Project, slug=slug)
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()
    previous_project = Project.objects.filter(id__lt=project.id).order_by('-id').first()  # type: ignore[union-attr]
    next_project = Project.objects.filter(id__gt=project.id).order_by('id').first()  # type: ignore[union-attr]
    context = {
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        'project': project,
        'project_categories': project_categories,
        "news_categories": news_categories,
        'previous_project': previous_project,
        'next_project': next_project,
    }
    return render(request, 'detail_view.html', context)

def category(request, slug):
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-id')[:1]
    news = News.objects.order_by('-id')[1:4]
    projects = Project.objects.filter(category__slug=slug)
    project_category = get_object_or_404(ProjectCategory, slug=slug)
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()
    paginator = Paginator(projects, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'new_products': new_products,
        'news': news,
        'first_news': first_news,
        'project_category': project_category,
        'project_categories': project_categories,
        "news_categories": news_categories,
        'page_obj': page_obj
    }
    return render(request, 'category.html', context=context)