from django.views import generic
from django.template import Context, loader
from django.views.generic.edit import FormView

from boto import ses

from contact.forms import ContactForm

class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = 'submit/'

    def form_valid(self, form):
        conn = ses.connect_to_region('us-east-1')

        conn.send_email(
            '{} <no-reply@danehillard.com>'.format(form.cleaned_data.get('name')),
            form.cleaned_data.get('subject'),
            form.cleaned_data.get('message') + '\n-' + form.cleaned_data.get('name'),
            'contact@danehillard.com',
            reply_addresses = (form.cleaned_data.get('email'),),
        )

        conn.send_email(
            'Dane Hillard Photography <no-reply@danehillard.com>',
            'Thank you for contacting dHP!',
            loader.get_template('contact/contact_thank_you.html').render(Context({})).strip(),
            form.cleaned_data.get('email'),
            format='html'
        )

        return super(ContactFormView, self).form_valid(form)

class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
