from django.urls import path
from .views import news, news_category, news_detail

app_name = 'news'

urlpatterns = [
    path('', news, name='news'),
    path('category/<str:slug>/', news_category, name='news_category'),
    path('<str:slug>/', news_detail, name='news_detail'),
]