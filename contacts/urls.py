from django.urls import path
from .views import contacts

app_name = 'contact-us'

urlpatterns = [
    path('', contacts, name='contact-us')
]