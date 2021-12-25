from taggit.models import Tag

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class StaticViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return ['about_me']

    def location(self, obj):
        return reverse(obj)


class PostViewSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Post.objects.all().filter(publish=True)

    def lastmod(self, obj):
        return obj.published_at


class TagViewSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Tag.objects.all()


