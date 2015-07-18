from django.template import Library
from django.core.urlresolvers import reverse

register = Library()


@register.inclusion_tag('social/feedly.html', takes_context=True)
def feedly_button(context, url=None):
    if not url:
        url = '{}://{}{}'.format(context['request'].scheme, context['request'].META.get('HTTP_HOST'), reverse('feed'))
    return {'url': url}