"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductsSitemap, NewsSitemap, ProjectSitemap, StaticViewSitemap, CategoriesSitemap, TypeSitemap, ProjectCategorySitemap

sitemaps = {
    'products': ProductsSitemap,
    'news': NewsSitemap,
    'projects': ProjectSitemap,
    'static': StaticViewSitemap,
    'categories': CategoriesSitemap,
    'type': TypeSitemap,
    'project_categories': ProjectCategorySitemap,
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('products/', include('products.urls')),
    path('projects/', include('projects.urls')),
    path('news/', include('news.urls')),
    path('dah-solar/', include('dahsolar.urls')),
    path('contact-us/', include('contacts.urls')),
    prefix_default_language=False,
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
