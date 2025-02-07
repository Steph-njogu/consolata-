import markdown
from django.utils.safestring import mark_safe
from django import template
from seminary.models import Room  # Import your model here

register = template.Library()

@register.filter(name='markdown')
def markdown_format(value):
    if isinstance(value, Room):
        value = value.content  # Assuming 'content' is the field you want to render
    return mark_safe(markdown.markdown(value))
