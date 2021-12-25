from django.urls import path

from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='new_post'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.SearchPost.as_view(), name='post_search'),
    path('<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('<slug:slug>/update/', views.UpdatePostView.as_view(), name='post_update'),
    path('tags/<slug:tag_slug>/', views.tagged, name='post_list_by_tags'),
    path('<slug:slug>/delete', views.PostDeleteView.as_view(), name='post_delete'),
 ]
