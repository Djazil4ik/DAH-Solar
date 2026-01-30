from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Type, Brand, Products, Categories, ProductsImage, ProductsAdvantage, ProductsFAQ, ProductsDescriptionImage, Second_Category, HotProduct
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Second_Category)
admin.site.register(Categories)


class ProductsImageInline(admin.TabularInline):
    model = ProductsImage
    extra = 1


class ProductsAdvantageInline(admin.TabularInline):
    model = ProductsAdvantage
    extra = 1

class ProductsFAQInline(admin.TabularInline):
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
    inlines = [ProductsImageInline, ProductsAdvantageInline,
               ProductsFAQInline, ProductsDescriptionImageInline, SecondCategoryInline]
    list_display = ('prod_model',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(HotProduct)
class HotProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order')
    list_editable = ('order',)
