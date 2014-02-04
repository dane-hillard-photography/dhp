from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from sitemaps import PhotographSitemap, AlbumSitemap, SiteSitemap

from dhp import settings

admin.autodiscover()

sitemaps = {
    'photograph': PhotographSitemap,
    'album': AlbumSitemap,
    'pages': SiteSitemap(['home:home', 'photography:photography', 'contact:contact', 'music:music', 'about:about']),
}

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', include('home.urls', namespace='home')),
    url(r'^about/', include('about.urls', namespace='about')),
    url(r'^tools/dhpadmin/', include(admin.site.urls)),
    url(r'^photography/', include('photography.urls', namespace='photography')),
    url(r'^music/', include('music.urls', namespace='music')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'home/login.html' }),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps': sitemaps }),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
