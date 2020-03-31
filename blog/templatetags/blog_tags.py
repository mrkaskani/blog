from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/temp_tags/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.all().filter(publish=True).order_by('-published_at')[:count]
    return {'latest_posts': latest_posts}

