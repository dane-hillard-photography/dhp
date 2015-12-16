from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
from django.contrib.sitemaps.views import sitemap

from django.conf import settings

from dhp.feeds import LatestPostsFeed
from sitemaps import SiteSitemap, PostSitemap

sitemaps = {
    'pages': SiteSitemap(['home:home', 'contact:contact', 'about:about']),
    'posts': PostSitemap,
}

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^', include('blog.urls', namespace='blog')),
    url(r'^about/', include('about.urls', namespace='about')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^login/', login, {'template_name': 'home/login.html'}),
    url(r'^logout/', logout),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}),
    url(r'^feed/', LatestPostsFeed(), name='feed'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='not_found'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='server_error'),
        url(r'^branding/', include('branding.urls', namespace='branding')),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
