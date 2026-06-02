from celery import shared_task
from .models import ProjectCategory, Project, ProjectImage
from core.translation_utils import safe_translate, translate_html


@shared_task
def translate_project_category_task(category_id):
    category = ProjectCategory.objects.filter(id=category_id).first()
    if not category:
        return

    update_fields = {}

    if category.category_name:
        update_fields['category_name_ru'] = safe_translate(
            text=category.category_name, src='en', dest='ru')
        update_fields['category_name_uz'] = safe_translate(
            text=category.category_name, src='en', dest='uz')

    if update_fields:
        ProjectCategory.objects.filter(id=category_id).update(**update_fields)

@shared_task
def translate_project_task(project_id):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return

    update_fields = {}

    if project.project_name:
        update_fields['project_name_ru'] = safe_translate(
            text=project.project_name, src='en', dest='ru')
        update_fields['project_name_uz'] = safe_translate(
            text=project.project_name, src='en', dest='uz')

    if project.body_text:
        update_fields['body_text_ru'] = translate_html(
            html_content=project.body_text, src='en', dest='ru')
        update_fields['body_text_uz'] = translate_html(
            html_content=project.body_text, src='en', dest='uz')

    if update_fields:
        Project.objects.filter(id=project_id).update(**update_fields)

@shared_task
def translate_project_image_task(image_id):
    image = ProjectImage.objects.filter(id=image_id).first()
    if not image:
        return

    # Assuming there's a text field to translate, if not, this task might be unnecessary
    if hasattr(image, 'text') and image.text:
        ProjectImage.objects.filter(id=image_id).update(
            text_ru=translate_html(image.text, src='en', dest='ru'),
            text_uz=translate_html(image.text, src='en', dest='uz')
        )