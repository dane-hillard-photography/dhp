from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.urls import path

from configuration.feeds import LatestPostsFeed
from sitemaps import SiteSitemap, PostSitemap

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME

sitemaps = {
    'pages': SiteSitemap(['home:home', 'contact:contact', 'about:about', 'about:pricing', 'photography:portfolio']),
    'posts': PostSitemap,
}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^', include('blog.urls')),
    url(r'^', include('photography.urls')),
    url(r'^about/', include('about.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^login/', login, {'template_name': 'home/login.html'}, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^humans.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}),
    url(r'^feed/', LatestPostsFeed(), name='feed'),
    url(r'^branding/', include('branding.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='not_found'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='server_error'),
    ]

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
