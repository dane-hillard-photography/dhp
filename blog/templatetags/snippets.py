from django.template import Library

register = Library()


@register.inclusion_tag('blog/full_background_image.html')
def full_background_image(url):
    return {'url': url}