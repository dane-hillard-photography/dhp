from django.conf.urls import patterns, url

from contact import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ContactFormView.as_view(), name='contact'),
    url(r'^submit/$', views.ContactSubmitView.as_view(), name='submit'),
)
