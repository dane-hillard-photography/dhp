from django.conf import settings

SCRIPT_SOURCES = [
    "*.danehillard.com",
    "*.disqus.com",
    "*.disquscdn.com",
    "*.facebook.net",
    "*.google.com",
    "*.googleapis.com",
    "*.google-analytics.com",
    "*.gstatic.com",
    "*.instagram.com",
    "*.pinterest.com",
]

STYLE_SOURCES = [
    "*.danehillard.com",
    "*.disquscdn.com",
    "*.google.com",
    "*.googleapis.com",
]

FONT_SOURCES = [
    "*.gstatic.com",
    "*.danehillard.com",
]

FRAME_SOURCES = [
    "disqus.com",
    "*.disqus.com",
    "*.facebook.com",
    "*.google.com",
    "*.instagram.com",
]

IMAGE_SOURCES = [
    "*.danehillard.com",
    "*.disqus.com",
    "*.disquscdn.com",
    "*.doubleclick.net",
    "*.facebook.com",
    "*.google-analytics.com",
    "*.google.com",
    "*.pinterest.com",
]

PREFETCH_SOURCES = [
    "disqus.com",
    "*.disquscdn.com",
    "*.doubleclick.net",
    "*.googleapis.com",
    "*.google-analytics.com",
    "*.gstatic.com",
]

CONTENT_SECURITY_POLICY = {
    "script-src": f"'self' {' '.join(SCRIPT_SOURCES)} 'unsafe-inline' 'unsafe-eval'",
    "style-src": f"'self' {' '.join(STYLE_SOURCES)} 'unsafe-inline'",
    "font-src": f"'self' {' '.join(FONT_SOURCES)}",
    "frame-src": f"'self' {' '.join(FRAME_SOURCES)}",
    "img-src": f"'self' data: {' '.join(IMAGE_SOURCES)}",
    "prefetch-src": f"'self' {' '.join(PREFETCH_SOURCES)}",
}


def content_security_policy_middleware(get_response):
    def middleware(request):
        if not settings.DEBUG:
            CONTENT_SECURITY_POLICY["upgrade-insecure-requests"] = ""
        response = get_response(request)
        report_or_not = "-Report-Only" if getattr(settings, "CSP_REPORT_ONLY", False) else ""
        csp_header = f"Content-Security-Policy{report_or_not}"
        response[csp_header] = "; ".join(f"{key} {value}" for key, value in CONTENT_SECURITY_POLICY.items())
        return response

    return middleware
