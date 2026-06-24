from core.translation_utils import safe_translate, translate_html
from .models import NewsCategory, News, NewsImage
from celery import shared_task


@shared_task
def translate_news_category_task(category_id):
    category = NewsCategory.objects.get(id=category_id)
    if not category:
        return

    update_fields = {}

    if category.category_name:
        update_fields['category_name_ru'] = safe_translate(
            text=category.category_name, src='en', dest='ru')
        update_fields['category_name_uz'] = safe_translate(
            text=category.category_name, src='en', dest='uz')
        
    if update_fields:
        NewsCategory.objects.filter(id=category_id).update(**update_fields)


@shared_task
def translate_news_task(news_id):
    news = News.objects.get(id=news_id)
    if not news:
        return

    update_fields = {}

    if news.news_title:
        update_fields['news_title_ru'] = safe_translate(
            text=news.news_title, src='en', dest='ru')
        update_fields['news_title_uz'] = safe_translate(
            text=news.news_title, src='en', dest='uz')
        
    if update_fields:
        News.objects.filter(id=news_id).update(**update_fields)


@shared_task
def translate_news_image_task(image_id):
    image_obj = NewsImage.objects.filter(id=image_id).first()

    NewsImage.objects.filter(id=image_id).update(
        body_text_ru=translate_html(image_obj.body_text, src='en', dest='ru'), # type: ignore
        body_text_uz=translate_html(image_obj.body_text, src='en', dest='uz') # type: ignore
    )