from celery import shared_task
from .models import Products, ProductsAdvantage, ProductsFAQ, Type, Second_Category
from core.translation_utils import safe_translate, translate_html


@shared_task
def translate_product_task(product_id):
    product = Products.objects.filter(id=product_id).first()
    if not product:
        return

    update_fields = {}

    # Переводим sub_title, если он есть и еще не переведен (опционально)
    if product.sub_title:
        update_fields['sub_title_ru'] = safe_translate(
            text=product.sub_title, src='en', dest='ru')
        update_fields['sub_title_uz'] = safe_translate(
            text=product.sub_title, src='en', dest='uz')

    if product.advantages:
        update_fields['advantages_ru'] = safe_translate(
            text=product.advantages, src='en', dest='ru')
        update_fields['advantages_uz'] = safe_translate(
            text=product.advantages, src='en', dest='uz')
        
    if product.warranty:
        update_fields['warranty_ru'] = safe_translate(
            text=product.warranty, src='en', dest='ru')
        update_fields['warranty_uz'] = safe_translate(
            text=product.warranty, src='en', dest='uz')
    
    if product.payment:
        update_fields['payment_ru'] = safe_translate(
            text=product.payment, src='en', dest='ru')
        update_fields['payment_uz'] = safe_translate(
            text=product.payment, src='en', dest='uz')

    if update_fields:
        # .update() не вызывает метод save() модели и сигналы post_save
        Products.objects.filter(id=product_id).update(**update_fields)


@shared_task
def translate_advantage_task(advantage_id):
    obj = ProductsAdvantage.objects.filter(id=advantage_id).first()
    if not obj or not obj.advantage:
        return

    ProductsAdvantage.objects.filter(id=advantage_id).update(
        advantage_ru=translate_html(obj.advantage, src='en', dest='ru'),
        advantage_uz=translate_html(obj.advantage, src='en', dest='uz')
    )


@shared_task
def translate_faq_task(faq_id):
    obj = ProductsFAQ.objects.filter(id=faq_id).first()
    if not obj:
        return

    update_fields = {}
    if obj.faq:
        update_fields['faq_ru'] = safe_translate(
            text=obj.faq, src='en', dest='ru')
        update_fields['faq_uz'] = safe_translate(
            text=obj.faq, src='en', dest='uz')

    if obj.answer:
        update_fields['answer_ru'] = safe_translate(
            text=obj.answer, src='en', dest='ru')
        update_fields['answer_uz'] = safe_translate(
            text=obj.answer, src='en', dest='uz')

    if update_fields:
        ProductsFAQ.objects.filter(id=faq_id).update(**update_fields)


@shared_task
def translate_type_task(type_id):
    obj = Type.objects.filter(id=type_id).first()
    if not obj or not obj.product_type:
        return

    update_fields = {}
    if obj.product_type:
        update_fields['product_type_ru'] = safe_translate(
            text=obj.product_type, src='en', dest='ru')
        update_fields['product_type_uz'] = safe_translate(
            text=obj.product_type, src='en', dest='uz')

    if update_fields:
        Type.objects.filter(id=type_id).update(**update_fields)

@shared_task
def translate_second_category_task(sc_id):
    obj = Second_Category.objects.filter(id=sc_id).first()
    if not obj or not obj.second_category:
        return

    update_fields = {}
    if obj.second_category:
        update_fields['second_category_ru'] = safe_translate(
            text=obj.second_category, src='en', dest='ru')
        update_fields['second_category_uz'] = safe_translate(
            text=obj.second_category, src='en', dest='uz')
    
    if update_fields:
        Second_Category.objects.filter(id=sc_id).update(**update_fields)


@shared_task
def translate_category_task(category_id):
    from .models import Categories
    obj = Categories.objects.filter(id=category_id).first()
    if not obj or not obj.category:
        return

    update_fields = {}
    if obj.category:
        update_fields['category_ru'] = safe_translate(
            text=obj.category, src='en', dest='ru')
        update_fields['category_uz'] = safe_translate(
            text=obj.category, src='en', dest='uz')
    
    if update_fields:
        Categories.objects.filter(id=category_id).update(**update_fields)