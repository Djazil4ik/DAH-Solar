#products/models.py
from django.core.cache import cache
from django.db import models
from django.db import transaction
from django.utils.text import slugify
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    brand = models.CharField(max_length=255, verbose_name=_("Brand"))

    def __str__(self):
        return self.brand


class Categories(models.Model):
    category = models.CharField(max_length=255, verbose_name=_("Category"))
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name=_("Slug"))

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while Categories.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug
        super().save(*args, **kwargs)
        from .tasks import translate_category_task
        transaction.on_commit(lambda: translate_category_task.delay(self.id))  # type: ignore

    def __str__(self):
        return self.category


class Type(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1, related_name='types', verbose_name=_("Category")) #type: ignore
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name=_("Slug"))
    product_type = models.CharField(max_length=255, verbose_name=_("Product Type"))

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_type)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while Type.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)
        from .tasks import translate_type_task
        transaction.on_commit(
            lambda: translate_type_task.delay(self.id))  # type: ignore

    def __str__(self):
        return self.product_type


class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name=_("Category"))
    prod_model = models.CharField(max_length=255, verbose_name=_("Product Model"))
    sub_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Sub Title"))
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name=_("Brand"))
    prod_type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name=_("Product Type"))
    max_power = models.CharField(max_length=255, verbose_name=_("Maximum Power"))
    dimensions = models.CharField(max_length=255, verbose_name=_("Dimensions"))
    certificate = models.CharField(max_length=255, verbose_name=_("Certificate"))
    warranty = models.CharField(max_length=255, verbose_name=_("Warranty"))
    payment = models.CharField(max_length=255, verbose_name=_("Payment"))
    advantages = models.TextField(blank=True, null=True, verbose_name=_("Advantages"))
    doc_img = ResizedImageField(
        size=[1200, 900],
        quality=75,
        upload_to='products/webp/',
        force_format='WEBP',
        blank=True,
        null=True
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.prod_model)
            slug = base_slug
            num = 1

            # Проверяем, существует ли уже такой slug
            while Products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

        def _post_commit():
            from .tasks import translate_product_task
            translate_product_task.delay(self.id) #type: ignore
            cache.delete_pattern('category_*') #type: ignore
            cache.delete_pattern('product_detail_*') #type: ignore
            cache.delete_pattern('type_*') #type: ignore

        transaction.on_commit(_post_commit)

    def __str__(self):
        return self.prod_model


class HotProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  # Порядок вывода

    class Meta:
        ordering = ['order']


class ProductsImage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="products_images")
    image = ResizedImageField(
        size=[1200, 900],
        quality=75,
        upload_to='products/webp/',
        force_format='WEBP',
        blank=True,
        null=True
    )


class ProductsAdvantage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="products_advantages")
    advantage = RichTextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .tasks import translate_advantage_task
        transaction.on_commit(lambda: translate_advantage_task.delay(self.id))  # type: ignore


class ProductsDescriptionImage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="decription_images")
    image = models.ImageField()