from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class Categories(models.Model):
    category = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

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

    def __str__(self):
        return self.category


class Type(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1, related_name='types')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    product_type = models.CharField(max_length=255)

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

    def __str__(self):
        return self.product_type


class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    prod_model = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, default="default")
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    prod_type = models.ForeignKey('Type', on_delete=models.CASCADE)
    max_power = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    certificate = models.CharField(max_length=255)
    warranty = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
    advantages = models.TextField(null=True)
    doc_img = models.ImageField()
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

    def __str__(self):
        return self.prod_model


class HotProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  # Порядок вывода

    class Meta:
        ordering = ['order']  # Сначала сортируем по полю order

    def __str__(self):
        return f"Hot: {self.product.prod_model}"


class ProductsImage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="products_images")
    image = models.ImageField()


class ProductsAdvantage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="products_advantages")
    advantage = models.TextField(null=True)


class ProductsFAQ(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="faqs")
    faq = models.TextField(null=True)
    answer = models.TextField(null=True)


class ProductsDescriptionImage(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="decription_images")
    image = models.ImageField()


class Second_Category(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="second_category", null=True)
    second_category = models.CharField(max_length=255)

    def __str__(self):
        return self.second_category
