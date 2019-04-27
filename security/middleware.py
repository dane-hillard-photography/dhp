from django.conf import settings

DEFAULT_SOURCES = [
    'fonts.googleapis.com',
]

SCRIPT_SOURCES = [
    'ajax.googleapis.com',
    'assets.pinterest.com',
    'connect.facebook.net',
    'danehillard.disqus.com',
    'danehillard-dev.disqus.com',
    'log.pinterest.com',
    'platform.instagram.com',
    'www.instagram.com',
    'www.google-analytics.com',
    '*.disquscdn.com',
    'disqus.com',
    '*.google.com',
    '*.gstatic.com',
    '*.danehillard.com',
]

STYLE_SOURCES = [
    '*.disquscdn.com',
    'fonts.googleapis.com',
    'optimize.google.com',
    '*.danehillard.com',
]

FONT_SOURCES = [
    'fonts.gstatic.com',
    '*.danehillard.com',
]

FRAME_SOURCES = [
    'disqus.com',
    'staticxx.facebook.com',
    'www.facebook.com',
    'www.instagram.com',
    '*.google.com',
]

IMAGE_SOURCES = [
    '*.disquscdn.com',
    'referrer.disqus.com',
    'stats.g.doubleclick.net',
    'www.facebook.com',
    'www.google-analytics.com',
    'optimize.google.com',
    '*.danehillard.com',
]

PREFETCH_SOURCES = [
    'fonts.googleapis.com',
]

CONTENT_SECURITY_POLICY = {
    'default-src': f"'self' {' '.join(DEFAULT_SOURCES)}",
    'script-src': f"'self' {' '.join(SCRIPT_SOURCES)} 'unsafe-inline'",
    'style-src': f"'self' {' '.join(STYLE_SOURCES)} 'unsafe-inline'",
    'font-src': f"'self' {' '.join(FONT_SOURCES)}",
    'frame-src': f"'self' {' '.join(FRAME_SOURCES)}",
    'img-src': f"'self' data: {' '.join(IMAGE_SOURCES)}",
    'prefetch-src': f"'self' {' '.join(PREFETCH_SOURCES)}",
}


def content_security_policy_middleware(get_response):

    def middleware(request):
        if not settings.DEBUG:
            CONTENT_SECURITY_POLICY['upgrade-insecure-requests'] = ''
        response = get_response(request)
        report_or_not = '-Report-Only' if getattr(settings, 'CSP_REPORT_ONLY', False) else ''
        csp_header = f'Content-Security-Policy{report_or_not}'
        response[csp_header] = '; '.join(f'{key} {value}' for key, value in CONTENT_SECURITY_POLICY.items())
        return response

    return middleware
