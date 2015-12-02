from django.conf.urls import url

from contact import views

urlpatterns = [
    url(r'^$', views.ContactFormView.as_view(), name='contact'),
    url(r'^submit/$', views.ContactSubmitView.as_view(), name='submit'),
]
