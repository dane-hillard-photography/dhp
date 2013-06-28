from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

from home import views

urlpatterns = patterns('',
  url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
)
