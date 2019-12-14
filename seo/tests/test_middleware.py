from unittest.mock import Mock

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
        original_path = "foo"
        new_path = "bar"
        request = Mock()
        request.path = original_path

        middleware.REDIRECT_PATTERNS = {original_path: new_path}

        response = redirect_middleware(request)
        assert isinstance(response, HttpResponsePermanentRedirect)
        assert response.url == new_path

    def test_redirect_does_not_happen_when_path_does_not_match_pattern(self, redirect_middleware):
        request = Mock()
        request.path = "foo"

        middleware.REDIRECT_PATTERNS = {"bar": "baz"}

        response = redirect_middleware(request)
        assert not isinstance(response, HttpResponsePermanentRedirect)


class TestCrawlerMiddleware:
    @pytest.mark.parametrize(
        "user_agent,test_func",
        [
            ("Googlebot", middleware.is_google_crawler),
            ("Googlebot/2.1", middleware.is_google_crawler),
            (
                "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
                middleware.is_facebook_crawler,
            ),
            ("facebookexternalhit/1.1", middleware.is_facebook_crawler),
            ("Facebot", middleware.is_facebook_crawler),
            ("Twitterbot", middleware.is_twitter_crawler),
            ("Twitterbot/1.0", middleware.is_twitter_crawler),
        ],
    )
    def test_returns_true_for_correct_crawler(self, user_agent, test_func):
        assert test_func(user_agent)

    @pytest.mark.parametrize(
        "test_func", [middleware.is_google_crawler, middleware.is_facebook_crawler, middleware.is_twitter_crawler,]
    )
    def test_returns_false_for_unknown_crawler(self, test_func):
        assert not test_func("foo")

    @pytest.mark.parametrize("middleware_name", ["is_google_crawler", "is_facebook_crawler", "is_twitter_crawler",])
    def test_middleware_whitelists_crawler(self, middleware_name, crawler_middleware, monkeypatch):
        monkeypatch.setattr(middleware, middleware_name, lambda user_agent: True)
        request = Mock()
        crawler_middleware(request)
        assert request.is_whitelisted_crawler
