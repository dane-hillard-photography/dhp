from django.views import generic
from django.template import Context, loader
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from boto import ses
from django.conf import settings

from contact.forms import ContactForm


class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:submit')

    def form_valid(self, form):
        conn = ses.connect_to_region(
            'us-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        contact_name = form.cleaned_data.get('name', '')
        contact_first_name = contact_name.split(' ')[0] if contact_name else ''
        contact_email = form.cleaned_data.get('email')

        conn.send_email(
            source='{} <no-reply@danehillard.com>'.format(contact_name),
            subject=form.cleaned_data.get('subject'),
            body='{}\n\n-{}\n{}'.format(form.cleaned_data.get('message'), contact_name, form.cleaned_data.get('phone')),
            to_addresses='contact@danehillard.com',
            reply_addresses=[contact_email],
            format='text'
        )

        conn.send_email(
            source='Dane Hillard Photography <no-reply@danehillard.com>',
            subject='Thank you for contacting dHP!',
            body=loader.get_template('contact/contact_thank_you.html').render(Context({'name': contact_first_name})).strip(),
            to_addresses=contact_email,
            format='html'
        )

        return super(ContactFormView, self).form_valid(form)


class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
