from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_at', 'publish', )
    list_filter = ('title', 'body', )
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'approved_comment', )
    list_filter = ('active', 'created_at', )
    search_fields = ('author', 'email', 'body', )