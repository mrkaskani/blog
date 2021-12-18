from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.ListCreateAPIPost.as_view(), name='post_list_create'),
    path('<int:pk>/', views.RetrieveUpdateDestroyAPIPost.as_view(), name='post_detail'),
    path('<int:post_pk>/comments/', views.ListCreateAPIComment.as_view(), name='comment_list_create'),
    path('<int:post_pk>/comments/<int:pk>/', views.RetrieveUpdateDestroyAPIComment.as_view(), name='comment_detail'),
]
