from unittest import TestCase
from unittest.mock import Mock, patch

from django.http import HttpResponsePermanentRedirect

from seo import middleware


class RedirectMiddlewareTestCase(TestCase):

    def setUp(self):
        self.middleware = middleware.redirect_middleware(Mock())

    def test_redirect_happens_when_path_matches_pattern(self):
        original_path = 'foo'
        new_path = 'bar'
        request = Mock()
        request.path = original_path

        middleware.REDIRECT_PATTERNS = {original_path: new_path}

        response = self.middleware(request)
        self.assertIsInstance(response, HttpResponsePermanentRedirect)
        self.assertEqual(new_path, response.url)

    def test_redirect_does_not_happen_when_path_does_not_match_pattern(self):
        request = Mock()
        request.path = 'foo'

        middleware.REDIRECT_PATTERNS = {'bar': 'baz'}

        response = self.middleware(request)
        self.assertFalse(isinstance(response, HttpResponsePermanentRedirect))


class CrawlerMiddlewareTestCase(TestCase):

    def setUp(self):
        self.middleware = middleware.crawler_middleware(Mock())

    def test_is_google_crawler_when_google_crawler(self):
        user_agent = 'Googlebot'
        self.assertTrue(middleware.is_google_crawler(user_agent))
        user_agent = 'Googlebot/2.1'
        self.assertTrue(middleware.is_google_crawler(user_agent))

    def test_is_google_crawler_when_not_google_crawler(self):
        user_agent = 'foo'
        self.assertFalse(middleware.is_google_crawler(user_agent))

    def test_is_facebook_crawler_when_facebook_crawler(self):
        user_agent = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        self.assertTrue(middleware.is_facebook_crawler(user_agent))
        user_agent = 'facebookexternalhit/1.1'
        self.assertTrue(middleware.is_facebook_crawler(user_agent))
        user_agent = 'Facebot'
        self.assertTrue(middleware.is_facebook_crawler(user_agent))

    def test_is_facebook_crawler_when_not_facebook_crawler(self):
        user_agent = 'foo'
        self.assertFalse(middleware.is_facebook_crawler(user_agent))

    def test_is_twitter_crawler_when_google_crawler(self):
        user_agent = 'Twitterbot'
        self.assertTrue(middleware.is_twitter_crawler(user_agent))
        user_agent = 'Twitterbot/1.0'
        self.assertTrue(middleware.is_twitter_crawler(user_agent))

    def test_is_twitter_crawler_when_not_twitter_crawler(self):
        user_agent = 'foo'
        self.assertFalse(middleware.is_twitter_crawler(user_agent))

    @patch('seo.middleware.is_google_crawler')
    def test_middleware_when_is_google_crawler(self, is_google_crawler):
        is_google_crawler.return_value = True

        request = Mock()
        self.middleware(request)
        self.assertTrue(request.is_whitelisted_crawler)

    @patch('seo.middleware.is_facebook_crawler')
    def test_middleware_when_is_google_crawler(self, is_facebook_crawler):
        is_facebook_crawler.return_value = True

        request = Mock()
        self.middleware(request)
        self.assertTrue(request.is_whitelisted_crawler)

    @patch('seo.middleware.is_twitter_crawler')
    def test_middleware_when_is_google_crawler(self, is_twitter_crawler):
        is_twitter_crawler.return_value = True

        request = Mock()
        self.middleware(request)
        self.assertTrue(request.is_whitelisted_crawler)
