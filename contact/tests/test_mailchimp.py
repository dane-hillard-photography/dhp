import json

from unittest.mock import Mock, patch

from django.conf import settings

from contact.mailchimp import MailChimp


@patch('requests.post')
@patch('requests.get')
def test_subscribe_happy_path(get, post):
    subscription_response = Mock()
    subscription_response.status_code = 200
    post.return_value = subscription_response

    check = Mock()
    check.status_code = 200
    get.return_value = check

    MailChimp.subscribe('foo', 'bar', 'baz')

    post.assert_called_once_with(
        'https://us3.api.mailchimp.com/3.0/lists/{}/members'.format(settings.MAILCHIMP_LIST_ID),
        data=json.dumps({
            'email_address': 'foo',
            'status': 'pending',
            'merge_fields': {
                'FNAME': 'bar',
                'LNAME': 'baz',
            }
        }),
        auth=('foo', settings.MAILCHIMP_API_KEY)
    )

    get.assert_called_once_with(
        'https://us3.api.mailchimp.com/3.0/lists/{}/members/{}'.format(settings.MAILCHIMP_LIST_ID, 'acbd18db4cc2f85cedef654fccc4a4d8'),
    )

@patch('requests.post')
@patch('requests.get')
def test_subscribe_when_subscribe_fails(get, post):
    subscription_response = Mock()
    subscription_response.status_code = 500
    post.return_value = subscription_response

    MailChimp.subscribe('foo', 'bar', 'baz')

    post.assert_called_once_with(
        'https://us3.api.mailchimp.com/3.0/lists/{}/members'.format(settings.MAILCHIMP_LIST_ID),
        data=json.dumps({
            'email_address': 'foo',
            'status': 'pending',
            'merge_fields': {
                'FNAME': 'bar',
                'LNAME': 'baz',
            }
        }),
        auth=('foo', settings.MAILCHIMP_API_KEY)
    )

    assert get.call_count == 0
