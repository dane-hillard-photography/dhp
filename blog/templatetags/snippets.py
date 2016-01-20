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


@register.inclusion_tag('blog/responsive_image.html')
def image(filename):
    return {'photo': get_photo_by_filename(filename)}


@register.inclusion_tag('blog/background_image.html')
def background_image(filename):
    return {'photo': get_photo_by_filename(filename)}
