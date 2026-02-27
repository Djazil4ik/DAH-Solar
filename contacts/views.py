from django.shortcuts import render
from news.models import NewsCategory
from projects.models import ProjectCategory


def contacts(request):
    return render(request, 'contacts/contact.html')
