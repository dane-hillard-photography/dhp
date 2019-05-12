from unittest.mock import Mock, patch

from recaptcha import recaptcha_is_valid


@patch('requests.post')
def test_recaptcha_is_valid_when_valid(mock_response):
    request = Mock()
    request.POST = {'g-recaptcha-response': 'somejunk'}
    mock_response.json.return_value = {'success': True}
    assert recaptcha_is_valid(request)

@patch('requests.post')
def test_recaptcha_is_valid_when_invalid(mock_response):
    request = Mock()
    request.POST = {}
    assert not recaptcha_is_valid(request)
