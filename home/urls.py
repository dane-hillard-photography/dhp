from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
]
