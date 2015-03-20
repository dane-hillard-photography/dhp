from django.template import Library

register = Library()


@register.inclusion_tag('blog/fixed_background_image.html')
def fixed_background_image(url):
    return {'url': url}