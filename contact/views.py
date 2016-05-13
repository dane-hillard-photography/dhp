import logging

from django.conf import settings
from django.views import generic
from django.template import Context, loader
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from boto3.session import Session
from botocore.exceptions import ClientError

import requests

from contact.forms import ContactForm
from contact.mailchimp import MailChimp


class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:submit')

    @staticmethod
    def send_email(source='', to_addresses=None, reply_addresses=None, subject='', body='', email_format='html'):
        session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        client = session.client('ses', region_name='us-east-1')

        to_addresses = to_addresses or []
        reply_addresses = reply_addresses or []

        try:
            response = client.send_email(
                Source=source,
                Destination={
                    'ToAddresses': to_addresses,
                },
                Message={
                    'Subject': {
                        'Data': subject,
                    },
                    'Body': {
                        'Html' if email_format == 'html' else 'Text': {
                            'Data': body
                        }
                    }
                },
                ReplyToAddresses=reply_addresses,
            )
        except ClientError as e:
            logging.error('There was a problem sending email from {} to {}'.format(source, to_addresses))
            raise e

    def form_valid(self, form):
        contact_first_name = form.cleaned_data.get('first_name', '')
        contact_last_name = form.cleaned_data.get('last_name', '')
        contact_name = ' '.join((contact_first_name, contact_last_name))
        contact_email = form.cleaned_data.get('email')

        self.send_email(
            source='{} <no-reply@danehillard.com>'.format(contact_name),
            subject=form.cleaned_data.get('subject'),
            body='{}\n\n-{}\n{}'.format(form.cleaned_data.get('message'), contact_name, form.cleaned_data.get('phone')),
            to_addresses=['contact@danehillard.com'],
            reply_addresses=[contact_email],
            email_format='text'
        )

        self.send_email(
            source='Dane Hillard Photography <no-reply@danehillard.com>',
            subject='Thank you for contacting dHP!',
            body=loader.get_template('contact/contact_thank_you.html').render(Context({'name': contact_first_name})).strip(),
            to_addresses=[contact_email],
        )

        if form.cleaned_data.get('join_mailing_list'):
            MailChimp.subscribe_to_mailing_list(contact_email, contact_first_name, contact_last_name)

        return super(ContactFormView, self).form_valid(form)


class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
