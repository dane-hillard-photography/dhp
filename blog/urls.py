from django.conf.urls import url

from blog import views

app_name = "blog"

urlpatterns = [
    url(r"^post/(?P<slug>[\w\-]+)/$", views.post_view, name="post"),
]
