import re

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
