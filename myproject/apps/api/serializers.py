from django.urls import reverse
from rest_framework import serializers

from blog.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'body', 'created_at',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        # extra_kwargs = (
        #     {
        #         'author': {'write_only': True}
        #     }
        # )
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)
