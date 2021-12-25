from django.urls import path

from . import views


app_name = 'api'


urlpatterns = [
    path('', views.PostList.as_view(), name='serializer_post_list'),
    path('<int:pk>', views.PostDetail.as_view(), name='serializer_post_detail'),
]
