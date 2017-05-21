from django.views import generic
from django.template import Context, loader
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from contact.forms import ContactForm
from contact.mailchimp import MailChimp
from contact.email import send_email


class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:submit')

    def form_valid(self, form):
        contact_first_name = form.cleaned_data.get('first_name', '')
        contact_last_name = form.cleaned_data.get('last_name', '')
        contact_name = ' '.join((contact_first_name, contact_last_name))
        contact_email = form.cleaned_data.get('email')

        send_email(
            source='{} <no-reply@danehillard.com>'.format(contact_name),
            subject=form.cleaned_data.get('subject'),
            body='{}\n\n-{}\n{}'.format(form.cleaned_data.get('message'), contact_name, form.cleaned_data.get('phone')),
            to_addresses=['contact@danehillard.com'],
            reply_addresses=[contact_email],
            email_format='text'
        )

        send_email(
            source='Dane Hillard Photography <no-reply@danehillard.com>',
            subject='Thank you for contacting dHP!',
            body=loader.get_template('contact/contact_thank_you.html').render(Context({'name': contact_first_name})).strip(),
            to_addresses=[contact_email],
        )

        return super(ContactFormView, self).form_valid(form)


class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
