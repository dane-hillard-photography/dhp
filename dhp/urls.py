from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

from dhp import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', include('home.urls', namespace='home')),
    url(r'^about/', include('about.urls', namespace='about')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^photography/', include('photography.urls', namespace='photography')),
    url(r'^music/', include('music.urls', namespace='music')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
)
