from modeltranslation.translator import register, TranslationOptions 
from .models import NewsArticle

@register(NewsArticle)
class NewsArticleTranslationOptions(TranslationOptions):
    fields = ("title", "content")