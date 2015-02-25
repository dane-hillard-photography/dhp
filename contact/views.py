from django.views import generic
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
            'dHP bot <no-reply@danehillard.com>',
            'New message from ' + form.cleaned_data.get('name'),
            form.cleaned_data.get('message'),
            'contact@danehillard.com',
            reply_addresses = (form.cleaned_data.get('email')),
        )

        conn.send_email(
            'Dane Hillard Photography <contact@danehillard.com>',
            'Thank you for contacting dHP!',
            'Hey ' + form.cleaned_data.get('name') + """,
<br /><br />
Thanks for contacting me! If you requested further contact, you\'ll hear from me soon!
<br /><br />
Regards,
<br /><br />
Dane Hillard<br />
<a href="http://www.danehillard.com">dHP</a>
""",
            form.cleaned_data.get('email'),
            format='html'
        )

        return super(ContactFormView, self).form_valid(form)

class ContactSubmitView(generic.TemplateView):
    template_name = 'contact/submit.html'
