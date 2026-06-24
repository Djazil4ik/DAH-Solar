from modeltranslation.translator import register, TranslationOptions
from .models import News, NewsCategory, NewsImage

@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('news_title',)

@register(NewsImage)
class NewsImageTranslationOptions(TranslationOptions):
    fields = ('body_text',)