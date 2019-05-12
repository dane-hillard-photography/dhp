from unittest.mock import Mock, patch

import pytest
from django.http import HttpResponsePermanentRedirect

from seo import middleware

@pytest.fixture
def redirect_middleware():
    return middleware.redirect_middleware(Mock())


@pytest.fixture
def crawler_middleware():
    return middleware.crawler_middleware(Mock())


class TestRedirectMiddleware:
    def test_redirect_happens_when_path_matches_pattern(self, redirect_middleware):
        original_path = 'foo'
        new_path = 'bar'
        request = Mock()
        request.path = original_path

        middleware.REDIRECT_PATTERNS = {original_path: new_path}

        response = redirect_middleware(request)
        assert isinstance(response, HttpResponsePermanentRedirect)
        assert response.url == new_path

    def test_redirect_does_not_happen_when_path_does_not_match_pattern(self, redirect_middleware):
        request = Mock()
        request.path = 'foo'

        middleware.REDIRECT_PATTERNS = {'bar': 'baz'}

        response = redirect_middleware(request)
        assert not isinstance(response, HttpResponsePermanentRedirect)


class TestCrawlerMiddleware:
    def test_is_google_crawler_when_google_crawler(self, crawler_middleware):
        user_agent = 'Googlebot'
        assert middleware.is_google_crawler(user_agent)
        user_agent = 'Googlebot/2.1'
        assert middleware.is_google_crawler(user_agent)

    def test_is_google_crawler_when_not_google_crawler(self):
        user_agent = 'foo'
        assert not middleware.is_google_crawler(user_agent)

    def test_is_facebook_crawler_when_facebook_crawler(self):
        user_agent = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        assert middleware.is_facebook_crawler(user_agent)
        user_agent = 'facebookexternalhit/1.1'
        assert middleware.is_facebook_crawler(user_agent)
        user_agent = 'Facebot'
        assert middleware.is_facebook_crawler(user_agent)

    def test_is_facebook_crawler_when_not_facebook_crawler(self):
        user_agent = 'foo'
        assert not middleware.is_facebook_crawler(user_agent)

    def test_is_twitter_crawler_when_google_crawler(self):
        user_agent = 'Twitterbot'
        assert middleware.is_twitter_crawler(user_agent)
        user_agent = 'Twitterbot/1.0'
        assert middleware.is_twitter_crawler(user_agent)

    def test_is_twitter_crawler_when_not_twitter_crawler(self):
        user_agent = 'foo'
        assert not middleware.is_twitter_crawler(user_agent)

    @patch('seo.middleware.is_google_crawler')
    def test_middleware_when_is_google_crawler(self, is_google_crawler, crawler_middleware):
        is_google_crawler.return_value = True

        request = Mock()
        crawler_middleware(request)
        assert request.is_whitelisted_crawler

    @patch('seo.middleware.is_facebook_crawler')
    def test_middleware_when_is_google_crawler(self, is_facebook_crawler, crawler_middleware):
        is_facebook_crawler.return_value = True

        request = Mock()
        crawler_middleware(request)
        assert request.is_whitelisted_crawler

    @patch('seo.middleware.is_twitter_crawler')
    def test_middleware_when_is_google_crawler(self, is_twitter_crawler, crawler_middleware):
        is_twitter_crawler.return_value = True

        request = Mock()
        crawler_middleware(request)
        assert request.is_whitelisted_crawler
