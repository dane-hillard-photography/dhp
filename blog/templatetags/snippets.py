import logging

from django.template import Library

from photography.models import Photograph

register = Library()

logger = logging.getLogger(__name__)


def get_photo_by_filename(filename):
    try:
        return Photograph.objects.get(filename=filename)
    except Photograph.DoesNotExist:
        logger.warning('No photo with the filename \'{}\' exists!'.format(filename))


@register.inclusion_tag('blog/full_background_image.html')
def full_background_image(url, position=None, padding_override=None):
    return {'url': url, 'position': position, 'padding_override': padding_override}


@register.inclusion_tag('blog/responsive_image.html')
def image(filename):
    return {'photo': get_photo_by_filename(filename)}


@register.inclusion_tag('blog/full_background_image.html')
def background_image(filename):
    photo = get_photo_by_filename(filename)
    if photo:
        return {'url': photo.thumbnail_large.url}
