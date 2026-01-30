from django.urls import path
from .views import home, search_results

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path("search/", search_results, name="search_results"),
]