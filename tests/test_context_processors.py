from unittest.mock import Mock

from django.test import override_settings

from context_processors import template_visible_settings


def test_template_visible_settings(settings):
    settings.FOO = 'bar'
    settings.TEMPLATE_VISIBLE_SETTINGS = ('FOO',)

    request = Mock()
    assert template_visible_settings(request) == {'FOO': 'bar'}
