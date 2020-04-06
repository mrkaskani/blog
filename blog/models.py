from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


def post_directory_path(instance, filename):
    return 'post_{}/{}'.format(instance.title, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to=post_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    def published(self):
        self.publish = True
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    email = models.EmailField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at', )

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '{}'.format(self.body)


class Permissions(models.Model):
    class Meta:
        permissions = [
            ('car_view', 'Can View Post'),
            ('add_post', 'Can Add Post'),
            ('change_post', 'Can Change Post'),
            ('delete_post', 'Can Delete Post'),
            ('change_comment', 'Can Change Comment')
        ]
