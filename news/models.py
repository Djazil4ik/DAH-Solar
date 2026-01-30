from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify


class NewsCategory(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category_name)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class News(models.Model):
    news_title = models.CharField(max_length=255)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, related_name='news', null=True)
    created_at = models.DateTimeField(default=now)
    preview = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.news_title)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.news_title


class NewsImage(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True)
    body_text = models.TextField(blank=True, null=True)
