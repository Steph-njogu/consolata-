import markdown
from django.utils.safestring import mark_safe
from django import template
from blogs.models import NewsArticle  # Import your model here

register = template.Library()

@register.filter(name='markdown')
def markdown_format(value):
    if isinstance(value, NewsArticle):
        value = value.content  # Assuming 'content' is the field you want to render
    return mark_safe(markdown.markdown(value))
