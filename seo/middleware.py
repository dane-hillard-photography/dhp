import re
import logging

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


LOGGER = logging.getLogger(__name__)


REDIRECT_PATTERNS = {r"^/photography(/|$)": reverse("home:home")}


def is_facebook_crawler(user_agent):
    return user_agent in settings.WHITELISTED_CRAWLERS.get("facebook", [])


def is_twitter_crawler(user_agent):
    return user_agent in settings.WHITELISTED_CRAWLERS.get("twitter", [])


def is_google_crawler(user_agent):
    return user_agent in settings.WHITELISTED_CRAWLERS.get("google", [])


def redirect_middleware(get_response):
    def middleware(request):
        for pattern in REDIRECT_PATTERNS:
            if re.match(pattern, request.path):
                return HttpResponsePermanentRedirect(REDIRECT_PATTERNS[pattern])

        return get_response(request)

    return middleware


def crawler_middleware(get_response):
    def middleware(request):
        user_agent = request.META.get("HTTP_USER_AGENT")
        LOGGER.debug("Received request with user agent string '{}'".format(user_agent))

        request.is_whitelisted_crawler = any(
            [is_facebook_crawler(user_agent), is_twitter_crawler(user_agent), is_google_crawler(user_agent),]
        )
        LOGGER.debug("Request has {} whitelisted".format("been" if request.is_whitelisted_crawler else "not been"))

        return get_response(request)

    return middleware
