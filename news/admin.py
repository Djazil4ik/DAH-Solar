from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import News, NewsCategory, NewsImage

class NewsImageInline(admin.TabularInline):
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
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]
