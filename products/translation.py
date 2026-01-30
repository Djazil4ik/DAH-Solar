from modeltranslation.translator import register, TranslationOptions
from .models import Products, ProductsAdvantage, ProductsFAQ


@register(Products)
class ProductTranslationOptions(TranslationOptions):
    fields = ('sub_title', 'advantages',)

@register(ProductsAdvantage)
class ProductsAdvantageTranslationOptions(TranslationOptions):
    fields = ('advantage',)

@register(ProductsFAQ)
class ProductsFAQTranslationOptions(TranslationOptions):
    fields = ('faq', 'answer',)
