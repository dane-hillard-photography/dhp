import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuration.settings")
os.environ.setdefault("HTTPS", "on")

application = get_wsgi_application()
