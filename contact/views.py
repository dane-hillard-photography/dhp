from django.views import generic
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from boto import ses

from contact.forms import ContactForm

class ContactFormView(FormView):
    template_name = 'contact/index.html'
    form_class = ContactForm
    success_url = reverse('contact:submit')

    def form_valid(self, form):
        conn = ses.connect_to_region('us-east-1')

        contact_name = form.cleaned_data.get('name', '')
        contact_first_name = contact_name.split(' ')[0] if contact_name else ''
        contact_email = form.cleaned_data.get('email')

        conn.send_email(
            '{} <no-reply@danehillard.com>'.format(contact_name),
            form.cleaned_data.get('subject'),
            '{}\n\n-{}'.format(form.cleaned_data.get('message'), contact_name),
            'contact@danehillard.com',
            reply_addresses = (contact_email,),
        )

        conn.send_email(
            'Dane Hillard Photography <no-reply@danehillard.com>',
            'Thank you for contacting dHP!',
            loader.get_template('contact/contact_thank_you.html').render(Context({'name': contact_first_name})).strip(),
            contact_email,
            format='html'
        )

        return super(ContactFormView, self).form_valid(form)

class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
