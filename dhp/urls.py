from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings

from dhp.feeds import LatestPostsFeed
from sitemaps import PhotographSitemap, PhotoSetSitemap, SiteSitemap, PostSitemap

sitemaps = {
    'photoset': PhotoSetSitemap,
    'photograph': PhotographSitemap,
    'pages': SiteSitemap(['home:home', 'photography:photography', 'contact:contact', 'about:about']),
    'posts': PostSitemap,
}

urlpatterns = patterns(
    '',
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^$', include('home.urls', namespace='home')),
    url(r'^', include('blog.urls', namespace='blog')),
    url(r'^about/', include('about.urls', namespace='about')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^photography/', include('photography.urls', namespace='photography')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'home/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^feed/$', LatestPostsFeed(), name='feed'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='not_found'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='server_error'),
    )

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
