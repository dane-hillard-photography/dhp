import json
import hashlib
import logging

from django.conf import settings
from django.views import generic
from django.template import Context, loader
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from boto import ses

import requests

from contact.forms import ContactForm


class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:submit')

    def send_email(self, source=None, to_addresses=None, reply_addresses=None, subject=None, body=None, format=None):
        conn = ses.connect_to_region(
            'us-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        result = conn.send_email(
            source=source,
            subject=subject,
            body=body,
            to_addresses=to_addresses,
            reply_addresses=reply_addresses,
            format=format,
        )

        if 'ErrorResponse' in result:
            logging.error(result.get('ErrorResponse', {}).get('Error', {}).get('Message',''))

    def form_valid(self, form):
        contact_first_name = form.cleaned_data.get('first_name', '')
        contact_last_name = form.cleaned_data.get('last_name', '')
        contact_name = ' '.join((contact_first_name, contact_last_name))
        contact_email = form.cleaned_data.get('email')

        self.send_email(
            source='{} <no-reply@danehillard.com>'.format(contact_name),
            subject=form.cleaned_data.get('subject'),
            body='{}\n\n-{}\n{}'.format(form.cleaned_data.get('message'), contact_name, form.cleaned_data.get('phone')),
            to_addresses='contact@danehillard.com',
            reply_addresses=[contact_email],
            format='text'
        )

        self.send_email(
            source='Dane Hillard Photography <no-reply@danehillard.com>',
            subject='Thank you for contacting dHP!',
            body=loader.get_template('contact/contact_thank_you.html').render(Context({'name': contact_first_name})).strip(),
            to_addresses=contact_email,
            format='html'
        )

        if form.cleaned_data.get('join_mailing_list'):
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

        return super(ContactFormView, self).form_valid(form)


class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
