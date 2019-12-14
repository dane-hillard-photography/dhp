from unittest import mock

from django.http import HttpResponse

from security.middleware import content_security_policy_middleware


def mock_get_response(request):
    return HttpResponse()


def test_content_security_policy_middleware_when_report_only(settings):
    settings.CSP_REPORT_ONLY = True

    request = mock.Mock()

    response = content_security_policy_middleware(mock_get_response)(request)

    assert response.has_header("Content-Security-Policy-Report-Only")


def test_content_security_policy_middleware_when_enforced(settings):
    settings.CSP_REPORT_ONLY = False

    request = mock.Mock()

    response = content_security_policy_middleware(mock_get_response)(request)

    assert response.has_header("Content-Security-Policy")


def test_upgrade_insecure_requests_when_not_debug(settings):
    settings.DEBUG = False

    request = mock.Mock()

    response = content_security_policy_middleware(mock_get_response)(request)

    assert "upgrade-insecure-requests" in response["Content-Security-Policy"]
