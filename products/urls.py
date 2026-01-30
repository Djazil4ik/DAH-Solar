from django.urls import path
from .views import products, detail_view, category_view, type_view
app_name = 'products'

urlpatterns = [
     path('', products, name='products'),
     path('<str:slug>/', detail_view, name='product_detail'),
     path('category/<str:slug>/', category_view, name='category'),     
     path('category/<str:category_slug>/<str:slug>/', type_view, name='type'),
]