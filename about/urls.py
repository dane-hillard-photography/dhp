from django.conf.urls import url

from about import views

urlpatterns = [
    url(r'^$', views.AboutView.as_view(), name='about'),
]
