from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory
from django.core.paginator import Paginator

def projects(request):
    projects_list = Project.objects.all().order_by('-id')
    paginator = Paginator(projects_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'projects.html', {'page_obj': page_obj})


def detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Навигация: предыдущий и следующий проекты
    previous_project = Project.objects.filter(id__lt=project.id).order_by('-id').first() #type: ignore
    next_project = Project.objects.filter(id__gt=project.id).order_by('id').first() #type: ignore
    
    context = {
        'project': project,
        'previous_project': previous_project,
        'next_project': next_project,
    }
    return render(request, 'detail_view.html', context)


def category(request, slug):
    project_category = get_object_or_404(ProjectCategory, slug=slug)
    projects_list = Project.objects.filter(category=project_category).order_by('-id')
    
    paginator = Paginator(projects_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'project_category': project_category,
        'page_obj': page_obj
    }
    return render(request, 'category.html', context)