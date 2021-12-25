from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    title = 'My Blog'
    link = ''
    description = 'New Posts of my blog'

    def items(self):
        return Post.objects.all().filter(publish=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
