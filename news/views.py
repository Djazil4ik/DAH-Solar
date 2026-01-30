from .models import News, NewsCategory
from projects.models import ProjectCategory
from products.models import Products
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.
def news(request):
    news_list = News.objects.order_by('-created_at')
    news_categories = NewsCategory.objects.all()
    paginator = Paginator(news_list, 6)  # Show 6 news per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-created_at')[:1]
    news = News.objects.order_by('-created_at')[1:4]
    project_categories = ProjectCategory.objects.all()
    context = {
        'news_list': news_list,
        'news_categories': news_categories,
        'news': news,
        'first_news': first_news,
        'new_products': new_products,
        'page_obj': page_obj,
        'project_categories': project_categories,
    }
    return render(request, 'news.html', context=context)

def news_category(request, slug):
    news_list = News.objects.filter(category__slug=slug).order_by('-created_at')
    news_categories = NewsCategory.objects.all()
    news_category = get_object_or_404(NewsCategory, slug=slug)
    paginator = Paginator(news_list, 6)  # Show 6 news per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-created_at')[:1]
    news = News.objects.order_by('-created_at')[1:4]
    project_categories = ProjectCategory.objects.all()
    context = {
        'news_list': news_list,
        'news_categories': news_categories,
        'news_category': news_category,
        'news': news,
        'first_news': first_news,
        'new_products': new_products,
        'page_obj': page_obj,
        'project_categories': project_categories,
    }
    return render(request, 'news_category.html', context=context)

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    news_categories = NewsCategory.objects.all()
    new_products = Products.objects.order_by('-id')[:4]
    first_news = News.objects.order_by('-created_at')[:1]
    news = News.objects.order_by('-created_at')[1:4]
    project_categories = ProjectCategory.objects.all()
    previous_news = News.objects.filter(id__lt=news_item.id).order_by('-id').first()  # type: ignore[union-attr]
    next_news = News.objects.filter(id__gt=news_item.id).order_by('id').first()  # type: ignore[union-attr]
    context = {
        'news_item': news_item,
        'news_categories': news_categories,
        'news': news,
        'first_news': first_news,
        'new_products': new_products,
        'project_categories': project_categories,
        'previous_news': previous_news,
        'next_news': next_news,
    }
    return render(request, 'news_detail.html', context=context)
