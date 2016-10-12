from unittest import TestCase
from unittest.mock import Mock

from django.test import override_settings

from context_processors import template_visible_settings


class ContextProcessorTestCase(TestCase):

    @override_settings(TEMPLATE_VISIBLE_SETTINGS=('FOO',), FOO='bar')
    def test_template_visible_settings(self):
        request = Mock()
        self.assertDictEqual({'FOO': 'bar'}, template_visible_settings(request))
