from django.conf.urls import url

from branding import views

urlpatterns = [
    url(r'^$', views.BrandingView.as_view(), name='branding'),
]
