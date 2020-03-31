from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('about/', views.about_me, name='about_me'),
    path('', views.post_list, name='post_list'),
    path('post/tags/<slug:tag_slug>/', views.post_list, name='post_list_by_tags'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('create/', views.new_post, name='new_post'),
    path('post/update/<slug:slug>/', views.update_post, name='post_update'),
    path('post/delete/<slug:slug>/', views.delete_post, name='post_delete'),
    path('drafts/', views.draft_list_view, name='draft_list'),
]
