from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from blog.sitemaps import StaticViewSitemap, PostViewSitemaps

sitemaps = {
    'static': StaticViewSitemap, 'posts': PostViewSitemaps,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},  name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain'))
]

# i18n configure
urlpatterns += i18n_patterns(path('accounts/', include('account.urls')), prefix_default_language=False)

# media configure
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
