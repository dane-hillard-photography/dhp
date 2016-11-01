CONTENT_SECURITY_POLICY = {
    'default-src': "'self'",
    'script-src': "'self' connect.facebook.net assets.pinterest.com danehillard.disqus.com danehillard-dev.disqus.com log.pinterest.com www.google-analytics.com platform.instagram.com 'unsafe-inline'",
    'style-src': "'self' fonts.googleapis.com a.disquscdn.com 'unsafe-inline'",
    'font-src': "'self' fonts.gstatic.com",
    'frame-src': "'self' staticxx.facebook.com www.facebook.com www.instagram.com disqus.com",
    'img-src': "'self' data: www.facebook.com referrer.disqus.com a.disquscdn.com www.google-analytics.com",
}


class ContentSecurityPolicyMiddleware(object):

    def process_response(self, request, response):
        response['Content-Security-Policy'] = '; '.join(('{} {}'.format(key, value) for key, value in CONTENT_SECURITY_POLICY.items()))
        return response


class ContentTypeOptionsMiddleware(object):

    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        return response


class HSTSMiddleware(object):

    def process_response(self, request, response):
        response['Strict-Transport-Security'] = 'max-age=31536000'
        return response
