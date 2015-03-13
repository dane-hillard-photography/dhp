import markdown

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def to_markdown(value):
    return mark_safe(markdown.markdown(value))