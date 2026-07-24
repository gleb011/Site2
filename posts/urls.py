from django.urls import path
from posts.views import HomePage, CreatePost, LikePost, PostDetail, RepostPost, ReviewPost

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('post_create/', CreatePost.as_view(), name='post_create'),
    path('like/', LikePost.as_view(), name='like'),
    path('repost/', RepostPost.as_view(), name='repost'),
    path('review/', ReviewPost.as_view(), name='review'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
] 