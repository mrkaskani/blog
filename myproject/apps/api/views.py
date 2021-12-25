from rest_framework import generics

from ..blog.models import Post
from .serailizer import PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(publish=True)
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.filter(publish=True)
    serializer_class = PostSerializer
