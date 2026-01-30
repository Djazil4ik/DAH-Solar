from django.shortcuts import render
from news.models import NewsCategory
from projects.models import ProjectCategory


def contacts(request):
    project_categories = ProjectCategory.objects.all()
    news_categories = NewsCategory.objects.all()
    context = {
        'project_categories': project_categories,
        'news_categories': news_categories,
    }
    return render(request, 'contacts/contact.html', context=context)
