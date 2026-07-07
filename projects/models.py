from django.db import models
from django.db import transaction
from django.utils.timezone import now
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _


class ProjectCategory(models.Model):
    category_name = models.CharField(max_length=255, verbose_name=_("Category Name"))
    slug = models.SlugField(unique=False, blank=True, null=True, verbose_name=_("Slug"))


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
        from .tasks import translate_project_category_task
        transaction.on_commit(lambda: translate_project_category_task.delay(self.id))  # type: ignore
        translate_project_category_task.delay(self.id) #type: ignore
        

    def __str__(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=255, verbose_name=_("Project Name"))
    subtitle = models.TextField(null=True, blank=True, verbose_name=_("Subtitle"))
    body_text = RichTextField(verbose_name=_("Body Text"))
    date = models.DateTimeField(default=now, verbose_name=_("Date"))
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects', null=True, blank=True, verbose_name=_("Category")  )
    slug = models.SlugField(max_length=255, unique=True, blank=True,  null=True, verbose_name=_("Slug"))

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
        from .tasks import translate_project_task
        transaction.on_commit(lambda: translate_project_task.delay(self.id))  # type: ignore
        translate_project_task.delay(self.id) #type: ignore

    def __str__(self):
        return self.project_name


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(size=[1920, 1080], upload_to='projects/images/', verbose_name=_("Image"), force_format="WEBP", quality=75)
    text = RichTextField(null=True, blank=True, verbose_name=_("Text"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .tasks import translate_project_image_task
        transaction.on_commit(lambda: translate_project_image_task.delay(self.id))  # type: ignore
        translate_project_image_task.delay(self.id) #type: ignore
