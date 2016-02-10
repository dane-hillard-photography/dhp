import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect


REDIRECT_PATTERNS = {
    r'^/photography(/|$)': reverse('home:home')
}


class RedirectMiddleware(object):
    def process_request(self, request):
        for pattern in REDIRECT_PATTERNS:
            if re.match(pattern, request.path):
                return HttpResponsePermanentRedirect(REDIRECT_PATTERNS[pattern])


class CrawlerMiddleware(object):
    @staticmethod
    def is_facebook_crawler(user_agent):
        return user_agent in settings.WHITELISTED_CRAWLERS.get('facebook', [])

    @staticmethod
    def is_twitter_crawler(user_agent):
        return user_agent in settings.WHITELISTED_CRAWLERS.get('twitter', [])

    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        request.is_whitelisted_crawler = self.is_facebook_crawler(user_agent) or self.is_twitter_crawler(user_agent)
