from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^post/(?P<slug>[\w\-]+)/$', views.post_view, name='post'),
    url(r'^instant$', views.instant_article_view, name='instant_article'),
]
