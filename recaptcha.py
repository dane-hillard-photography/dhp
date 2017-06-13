import requests

from django.conf import settings


def recaptcha_is_valid(request):
    recaptcha_payload = request.POST.get('g-recaptcha-response')
    if recaptcha_payload:
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_payload,
                'remoteip': request.META.get('REMOTE_ADDR'),
            },
        )

        return recaptcha_response.json().get('success')
    else:
        return False
