import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuration.settings")
os.environ.setdefault('HTTPS', 'on')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
