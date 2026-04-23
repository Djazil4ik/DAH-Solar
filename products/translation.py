from modeltranslation.translator import register, TranslationOptions
from .models import Products, ProductsAdvantage, ProductsFAQ, Type, Second_Category, Categories


@register(Products)
class ProductTranslationOptions(TranslationOptions):
    fields = ('sub_title', 'advantages', 'warranty', 'payment',)


@register(ProductsAdvantage)
class ProductsAdvantageTranslationOptions(TranslationOptions):
    fields = ('advantage',)


@register(ProductsFAQ)
class ProductsFAQTranslationOptions(TranslationOptions):
    fields = ('faq', 'answer',)


@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('product_type',)


@register(Second_Category)
class SecondCategoryTranslationOptions(TranslationOptions):
    fields = ('second_category',)

@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('category',)