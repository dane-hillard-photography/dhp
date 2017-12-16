from django.conf.urls import url

from about import views

app_name = 'about'

urlpatterns = [
    url(r'^$', views.AboutView.as_view(), name='about'),
    url(r'^pricing', views.PricingView.as_view(), name='pricing'),
]
