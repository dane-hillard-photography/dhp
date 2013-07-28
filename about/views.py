from django.views import generic

import time

class AboutView(generic.TemplateView):
  template_name = 'about/index.html'
