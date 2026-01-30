from django.urls import path
from .views import projects, detail_view, category

app_name = 'projects'

urlpatterns = [
    path('', projects, name='projects'),
    path('<slug:slug>/', detail_view, name='detail_view'),
    path('category/<slug:slug>/', category, name='category_view'),
]