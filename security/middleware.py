from django.conf import settings


SCRIPT_SOURCES = [
    'ajax.googleapis.com',
    'assets.pinterest.com',
    'connect.facebook.net',
    'danehillard.disqus.com',
    'danehillard-dev.disqus.com',
    'log.pinterest.com',
    'platform.instagram.com',
    'www.google-analytics.com',
    'optimize.google.com',
    'disqus.com',
]

STYLE_SOURCES = [
    'disquscdn.com',
    'fonts.googleapis.com',
    'optimize.google.com',
]

FONT_SOURCES = [
    'fonts.gstatic.com',
]

FRAME_SOURCES = [
    'disqus.com',
    'staticxx.facebook.com',
    'www.facebook.com',
    'www.instagram.com',
    'optimize.google.com',
]

IMAGE_SOURCES = [
    'a.disquscdn.com',
    'referrer.disqus.com',
    'stats.g.doubleclick.net',
    'www.facebook.com',
    'www.google-analytics.com',
    'optimize.google.com',
]

CONTENT_SECURITY_POLICY = {
    'default-src': "'self'",
    'script-src': "'self' {} 'unsafe-inline'".format(' '.join(SCRIPT_SOURCES)),
    'style-src': "'self' {} 'unsafe-inline'".format(' '.join(STYLE_SOURCES)),
    'font-src': "'self' {}".format(' '.join(FONT_SOURCES)),
    'frame-src': "'self' {}".format(' '.join(FRAME_SOURCES)),
    'img-src': "'self' data: {}".format(' '.join(IMAGE_SOURCES)),
}


class ContentSecurityPolicyMiddleware(object):

    def process_response(self, request, response):
        csp_header = 'Content-Security-Policy{report_only}'.format(report_only='-Report-Only' if getattr(settings, 'CSP_REPORT_ONLY', False) else '')
        response[csp_header] = '; '.join(('{} {}'.format(key, value) for key, value in CONTENT_SECURITY_POLICY.items()))
        return response
