from unittest import mock

from django.http import HttpResponse
from django.test import TestCase

from security.middleware import content_security_policy_middleware


def mock_get_response(request):
    return HttpResponse()


class SecurityMiddlewareTestCase(TestCase):
    def test_content_security_policy_middleware_when_report_only(self):
        request = mock.Mock()

        with self.settings(CSP_REPORT_ONLY=True):
            response = content_security_policy_middleware(mock_get_response)(request)

        self.assertTrue(response.has_header('Content-Security-Policy-Report-Only'))

    def test_content_security_policy_middleware_when_enforced(self):
        request = mock.Mock()

        with self.settings(CSP_REPORT_ONLY=False):
            response = content_security_policy_middleware(mock_get_response)(request)

        self.assertTrue(response.has_header('Content-Security-Policy'))

    def test_upgrade_insecure_requests_when_not_debug(self):
        request = mock.Mock()

        with self.settings(DEBUG=False):
            response = content_security_policy_middleware(mock_get_response)(request)

        self.assertIn('upgrade-insecure-requests', response['Content-Security-Policy'])
