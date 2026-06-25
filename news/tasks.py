from core.translation_utils import safe_translate, translate_html
from .models import NewsCategory, News, NewsImage
from celery import shared_task


@shared_task
def translate_news_category_task(category_id):
    category = NewsCategory.objects.get(id=category_id)

    update_fields = {}

    if category.category_name:
        if not category.category_name_ru: #type: ignore
            update_fields['category_name_ru'] = safe_translate(
                text=category.category_name, src='en', dest='ru')
        if not category.category_name_uz: #type: ignore
            update_fields['category_name_uz'] = safe_translate(
                text=category.category_name, src='en', dest='uz')

    if update_fields:
        NewsCategory.objects.filter(id=category_id).update(**update_fields)


@shared_task
def translate_news_task(news_id):
    news = News.objects.get(id=news_id)

    update_fields = {}

    if news.news_title:
        if not news.news_title_ru: #type: ignore
            update_fields['news_title_ru'] = safe_translate(
                text=news.news_title, src='en', dest='ru')
        if not news.news_title_uz: #type: ignore
            update_fields['news_title_uz'] = safe_translate(
                text=news.news_title, src='en', dest='uz')

    if update_fields:
        News.objects.filter(id=news_id).update(**update_fields)


@shared_task
def translate_news_image_task(image_id):
    image_obj = NewsImage.objects.filter(id=image_id).first()
    if not image_obj or not image_obj.body_text:
        return

    update_fields = {}

    if not image_obj.body_text_ru: #type: ignore
        update_fields['body_text_ru'] = translate_html(
            image_obj.body_text, src='en', dest='ru')
    if not image_obj.body_text_uz: #type: ignore
        update_fields['body_text_uz'] = translate_html(
            image_obj.body_text, src='en', dest='uz')

    if update_fields:
        NewsImage.objects.filter(id=image_id).update(**update_fields)
