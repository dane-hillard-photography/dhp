from unittest import TestCase
from unittest.mock import Mock

from django.http import HttpResponsePermanentRedirect

from seo import middleware
from seo.middleware import RedirectMiddleware


class RedirectMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = RedirectMiddleware()

    def test_redirect_happens_when_path_matches_pattern(self):
        original_path = 'foo'
        new_path = 'bar'
        request = Mock()
        request.path = original_path

        middleware.REDIRECT_PATTERNS = {original_path: new_path}

        response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponsePermanentRedirect)
        self.assertEqual(new_path, response.url)

    def test_redirect_does_not_happen_when_path_does_not_match_pattern(self):
        request = Mock()
        request.path = 'foo'

        middleware.REDIRECT_PATTERNS = {'bar': 'baz'}

        response = self.middleware.process_request(request)
        self.assertIsNone(response)