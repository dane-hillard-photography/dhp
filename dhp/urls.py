from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from dhp import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dhp.views.home', name='home'),
    # url(r'^dhp/', include('dhp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', include('home.urls', namespace='home')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^photography/', include('photography.urls', namespace='photography')),
)
