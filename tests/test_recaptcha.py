from unittest import TestCase
from unittest.mock import Mock, patch

from recaptcha import recaptcha_is_valid


class RecaptchaTestCase(TestCase):
    @patch('requests.post')
    def test_recaptcha_is_valid_when_valid(self, mock_response):
        request = Mock()
        request.POST = {'g-recaptcha-response': 'somejunk'}
        mock_response.json.return_value = {'success': True}
        self.assertTrue(recaptcha_is_valid(request))

    @patch('requests.post')
    def test_recaptcha_is_valid_when_invalid(self, mock_response):
        request = Mock()
        request.POST = {}
        self.assertFalse(recaptcha_is_valid(request))
