from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from myproject.apps.blog import views

from myproject.apps.blog.sitemaps import PostViewSitemaps, StaticViewSitemap

sitemaps = {
    'posts': PostViewSitemaps, 'static': StaticViewSitemap,
}

urlpatterns = [
    # django administration
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # 3rd party
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registrations/', include('rest_auth.registration.urls')),

    # local app
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.About.as_view(), name='about_me'),
    path('posts/', include('myproject.apps.blog.urls', namespace='blog')),
    path('api/v1/', include('myproject.apps.api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
