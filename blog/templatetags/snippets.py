from django.template import Library

register = Library()


@register.inclusion_tag('blog/full_background_image.html')
def full_background_image(url, position=None, padding_override=None):
    return {'url': url, 'position': position, 'padding_override': padding_override}