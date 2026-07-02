from modeltranslation.translator import register, TranslationOptions
from .models import Products, ProductsAdvantage, Type, Categories


@register(Products)
class ProductTranslationOptions(TranslationOptions):
    fields = ('sub_title', 'advantages', 'warranty', 'payment',)


@register(ProductsAdvantage)
class ProductsAdvantageTranslationOptions(TranslationOptions):
    fields = ('advantage',)



@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('product_type',)


@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('category',)
