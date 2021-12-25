from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_at', 'publish', 'tags')
    list_filter = ('title', 'body',)
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('publish',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'post', 'created_at', 'approved_comment',)
    list_filter = ('approved_comment', 'created_at',)
    search_fields = ('author', 'email', 'body',)
