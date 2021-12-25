from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/temp_tags/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.all().filter(publish=True).order_by('-published_at')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/temp_tags/similar_posts.html')
def show_similar_posts(count=5):
    post_tags_ids = Post.objects.values_list('tags', flat=True)
    similar = Post.objects.filter(publish=True).filter(tags__in=post_tags_ids)
    similar_post = similar.annotate(same_tags=Count('tags')).order_by('-same_tags')[:count]
    return {'similar_post': similar_post}
