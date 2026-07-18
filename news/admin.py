from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import News, NewsCategory, NewsImage


class NewsImageInline(TranslationTabularInline):
    model = NewsImage
    extra = 1

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
    list_display = ('category_name',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('news_title', 'category', 'created_at', 'image_preview', 'slug')
    inlines = [NewsImageInline]

    def image_preview(self, obj):
        if obj.preview:
            return format_html('<img src="{}" width="180" height="auto" />', obj.preview.url)
        return "-"

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
