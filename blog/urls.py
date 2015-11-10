from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns(
    '',
    url(r'^post/(?P<slug>[\w\-]+)/$', views.post_view, name='post'),
    url(r'^archive/(?P<year>[0-9]{4})/$', views.PostYearArchiveView.as_view(), name='post_year_archive'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>0[1-9]|1[012])/$', views.PostMonthArchiveView.as_view(), name='post_month_archive'),
)
