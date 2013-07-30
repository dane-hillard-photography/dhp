from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views import generic
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
      form.cleaned_data.get('message') + '\n\n' + form.cleaned_data.get('email'),
      'contact@danehillard.com',
    )

    conn.send_email(
      'dHP bot <no-reply@danehillard.com>',
      'Thank you for contacting dHP!',
      form.cleaned_data.get('name') + """,
<br /><br />
Thank you for your message. If you requested further contact, you\'ll hear from me soon!
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
