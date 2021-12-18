from rest_framework import viewsets, permissions, generics
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment


class ListCreateAPIPost(generics.ListCreateAPIView):
    queryset = Post.objects.filter(publish=True)
    serializer_class = PostSerializer


class RetrieveUpdateDestroyAPIPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(publish=True)
    serializer_class = PostSerializer


class ListCreateAPIComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.queryset.filter(post_id=self.kwargs.get('post_pk')).filter(approved_comment=True)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post)


class RetrieveUpdateDestroyAPIComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(approved_comment=True)
    serializer_class = CommentSerializer
