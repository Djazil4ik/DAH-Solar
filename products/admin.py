from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Type, Brand, Products, Categories, ProductsImage,
    ProductsAdvantage, ProductsFAQ, ProductsDescriptionImage,
    Second_Category, HotProduct
)
from ckeditor.widgets import CKEditorWidget

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand',)
    search_fields = ('brand',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}
    search_fields = ('category',)


@admin.register(Type)
class TypeAdmin(TranslationAdmin):
    list_display = ('product_type', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('product_type',)}
    search_fields = ('product_type',)

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Second_Category)
class SecondCategoryAdmin(admin.ModelAdmin):
    list_display = ('second_category', 'product')
    list_filter = ('product',)
    search_fields = ('second_category',)


class ProductsImageInline(admin.TabularInline):
    model = ProductsImage
    extra = 1


class ProductsAdvantageInline(TranslationTabularInline):
    model = ProductsAdvantage
    extra = 1


class ProductsFAQInline(TranslationTabularInline):
    model = ProductsFAQ
    extra = 1


class ProductsDescriptionImageInline(admin.TabularInline):
    model = ProductsDescriptionImage
    extra = 1


class SecondCategoryInline(admin.TabularInline):
    model = Second_Category
    extra = 1


@admin.register(Products)
class ProductsAdmin(TranslationAdmin):
    inlines = [
        ProductsImageInline,
        ProductsAdvantageInline,
        ProductsFAQInline,
        ProductsDescriptionImageInline,
        SecondCategoryInline,
    ]
    list_display = ('prod_model', 'category', 'prod_type', 'brand')
    list_filter = ('category', 'prod_type', 'brand')
    search_fields = ('prod_model', 'sub_title')
    prepopulated_fields = {'slug': ('prod_model',)}

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(HotProduct)
class HotProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order')
    list_editable = ('order',)
