from django.urls import reverse
from django.core.cache import cache
from django.test import TestCase
from django.utils.text import slugify
from .models import Categories, Products, Brand, Type


class ProductModelTest(TestCase):
    def setUp(self):
        # Создаем базовые данные
        self.brand = Brand.objects.create(brand="DAH Solar")
        self.category = Categories.objects.create(category="Solar Panels")
        self.prod_type = Type.objects.create(
            category=self.category, product_type="Mono")

    def test_category_slug_generation(self):
        """Проверяем автоматическую генерацию слага категории"""
        cat = Categories.objects.create(category="Test Category")
        self.assertEqual(cat.slug, slugify("Test Category"))

    def test_duplicate_slug_handling(self):
        """Проверяем, что одинаковые названия не ломают уникальность слагов"""
        cat1 = Categories.objects.create(category="Solar")
        cat2 = Categories.objects.create(category="Solar")
        self.assertNotEqual(cat1.slug, cat2.slug)
        self.assertTrue(cat2.slug.startswith("solar-"))

    def test_product_creation(self):
        """Проверяем создание продукта и его слаг"""
        product = Products.objects.create(
            category=self.category,
            prod_model="DH-M60",
            brand=self.brand,
            prod_type=self.prod_type,
            max_power="450W",
            dimensions="120x90",
            certificate="ISO",
            warranty="25 years",
            payment="Cash/Card"
        )
        self.assertEqual(product.slug, slugify("DH-M60"))


class ProductViewTest(TestCase):
    def setUp(self):
        cache.clear()
        self.brand = Brand.objects.create(brand="DAH Solar")
        self.category = Categories.objects.create(
            category="Solar Panels", slug="solar-panels")
        self.prod_type = Type.objects.create(
            category=self.category, product_type="Mono", slug="mono")
        self.product = Products.objects.create(
            category=self.category,
            prod_model="DH-M60",
            brand=self.brand,
            prod_type=self.prod_type,
            slug="dh-m60",
            max_power="450W",
            dimensions="1:1",
            certificate="Yes",
            warranty="Full",
            payment="Any"
        )

    def test_products_list_view(self):
        """Тестируем основной список (имя 'products')"""
        # Используем namespace 'products:'
        response = self.client.get(reverse('products:products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_detail_view(self):
        """Тестируем страницу товара (имя 'product_detail')"""
        url = reverse('products:product_detail', kwargs={
                      'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

    def test_category_view(self):
        """Тестируем страницу категории (имя 'category')"""
        url = reverse('products:category', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_type_view(self):
        """Тестируем страницу типа товара (имя 'type' с двумя слагами)"""
        url = reverse('products:type', kwargs={
            'category_slug': self.category.slug,
            'slug': self.prod_type.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
