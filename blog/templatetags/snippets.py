import logging

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

logger = logging.getLogger(__name__)


@register.inclusion_tag('blog/full_background_image.html')
def full_background_image(url, position=None, padding_override=None):
    return {'url': url, 'position': position, 'padding_override': padding_override}


@register.inclusion_tag('blog/responsive_image.html', takes_context=True)
def image(context, filename):
    post = context.get('post')

    if post:
        try:
            photo = list(filter(lambda p: p.filename == filename, post.images.all()))[0]

            return {'photo': photo}
        except IndexError:
            logger.error('image templatetag was used without images attached to the post. URL: {}'.format(context.get('request').path))
            return None
