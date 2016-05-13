import json
import hashlib
import logging

from django.conf import settings

import requests


class MailChimp(object):
    @staticmethod
    def subscribe(contact_email, contact_first_name, contact_last_name):
        subscription_body = {
            'email_address': contact_email,
            'status': 'pending',
            'merge_fields': {
                'FNAME': contact_first_name,
                'LNAME': contact_last_name,
            }
        }

        subscription_response = requests.post(
            'https://us3.api.mailchimp.com/3.0/lists/{}/members'.format(settings.MAILCHIMP_LIST_ID),
            data=json.dumps(subscription_body),
            auth=('foo', settings.MAILCHIMP_API_KEY)
        )

        if subscription_response.status_code == 200:
            md5 = hashlib.md5()
            md5.update(contact_email.encode('utf-8'))
            member_id = md5.hexdigest()

            check = requests.get('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}'.format(
                settings.MAILCHIMP_LIST_ID,
                member_id
            ))

            if check.status_code != 200:
                logging.error('Subscription call was successful, but member \'{}\' does not appear to exist'.format(contact_email))
        else:
            logging.error('Unable to subscribe member \'{}\': {}'.format(contact_email, subscription_response.text))
