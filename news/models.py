from django.db import models, transaction
from django.utils.timezone import now
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class NewsCategory(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category_name)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while NewsCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)
        from .tasks import translate_news_category_task
        transaction.on_commit(lambda: translate_news_category_task.delay(self.id))  # type: ignore

    def __str__(self) -> str:
        return self.category_name


class News(models.Model):
    news_title = models.CharField(max_length=255)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, related_name='news', null=True)
    created_at = models.DateTimeField(default=now)
    preview = ResizedImageField(size=[1920, 1080], null=True, blank=True, verbose_name=_("Preview Image"), upload_to='news/previews/', force_format="WEBP", quality=75)
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
        from .tasks import translate_news_task
        transaction.on_commit(lambda: translate_news_task.delay(self.id))  # type: ignore

    def __str__(self) -> str:
        return self.news_title


class NewsImage(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(size=[1920, 1080], null=True, blank=True, verbose_name=_("Image"), upload_to='news/images/', force_format="WEBP", quality=75)
    body_text = RichTextField(null=True, blank=True, verbose_name=_("Body Text"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(f"!!! NewsImage.save() called, id={self.id}, body_text={bool(self.body_text)}") # type: ignore
        from .tasks import translate_news_image_task
        transaction.on_commit(lambda: translate_news_image_task.delay(self.id))  # type: ignore
