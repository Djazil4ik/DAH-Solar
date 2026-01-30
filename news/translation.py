from modeltranslation.translator import register, TranslationOptions
from .models import News, NewsCategory, NewsImage

@register(NewsCategory)
class NewsCategoryTrabslationOptions(TranslationOptions):
    fields = ('category_name',)