from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views import generic

import recaptcha
from contact.forms import ContactForm
from contact.email import send_email


class ContactFormView(generic.View):
    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            if not recaptcha.recaptcha_is_valid(request):
                form.add_error(None, ValidationError("Please complete the reCAPTCHA below"))
                return render(request, "contact/index.html", {"form": form,})

            contact_first_name = form.cleaned_data.get("first_name", "")
            contact_last_name = form.cleaned_data.get("last_name", "")
            contact_name = " ".join((contact_first_name, contact_last_name))
            contact_email = form.cleaned_data.get("email")

            send_email(
                source="{} <no-reply@danehillard.com>".format(contact_name),
                subject=form.cleaned_data.get("subject"),
                body="{}\n\n-{}\n{}".format(
                    form.cleaned_data.get("message"), contact_name, form.cleaned_data.get("phone")
                ),
                to_addresses=["contact@danehillard.com"],
                reply_addresses=[contact_email],
                email_format="text",
            )

            send_email(
                source="Dane Hillard Photography <no-reply@danehillard.com>",
                subject="Thank you for contacting dHP!",
                body=loader.get_template("contact/contact_thank_you.html").render({"name": contact_first_name}).strip(),
                to_addresses=[contact_email],
            )

            return redirect(reverse("contact:submit"))

    def get(self, request):
        return render(request, "contact/index.html", {"form": ContactForm()},)


class ContactSubmitView(generic.TemplateView):
    template_name = "contact/submit.html"
