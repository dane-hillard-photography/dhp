import os
import sys
import site

site.addsitedir('/var/www/.virtualenvs/myprojectenv/local/lib/python2.7/site-packages')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

os.environ['DJANGO_SETTINGS_MODULE'] = 'dhp.settings'

activate_env=os.path.expanduser("/var/www/.virtualenvs/dhp/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
