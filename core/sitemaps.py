from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from products.models import Categories, Type, Products
from news.models import News
from projects.models import Project, ProjectCategory

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["main:home", "dahsolar:dahsolar", "contact-us:contact-us"]

    def location(self, item):
        return reverse(item)

# Categories sitemap
class CategoriesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Categories.objects.all()

    def location(self, obj):
        return reverse("products:category", kwargs={"slug": obj.slug})

# Type sitemap
class TypeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Type.objects.all()

    def location(self, obj):
        return reverse("products:type", kwargs={"category_slug": obj.category.slug, "slug": obj.slug})

# Products sitemap
class ProductsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Products.objects.all()

    def location(self, obj):
        return reverse("products:product_detail", kwargs={"slug": obj.slug})

# News sitemap
class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return News.objects.all()

    def location(self, obj):
        return reverse("news:news_detail", kwargs={"slug": obj.slug})

# ProjectCategory sitemap
class ProjectCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ProjectCategory.objects.all()

    def location(self, obj):
        return reverse("projects:category_view", kwargs={"slug": obj.slug})

# Project sitemap
class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse("projects:detail_view", kwargs={"slug": obj.slug})