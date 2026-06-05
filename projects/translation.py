from modeltranslation.translator import register, TranslationOptions
from .models import ProjectCategory, Project, ProjectImage

@register(ProjectCategory)
class ProjectCategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('project_name', 'body_text', 'subtitle')

@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):
    fields = ('text',)