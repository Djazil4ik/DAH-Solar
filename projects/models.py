from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify


class ProjectCategory(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=False, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug не был задан вручную
            # Создаем базовый slug из названия категории
            base_slug = slugify(self.category_name)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while ProjectCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    body_text = models.TextField()
    date = models.DateTimeField(default=now)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True,  null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.project_name)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_name


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
    text = models.TextField(blank=True, null=True)
