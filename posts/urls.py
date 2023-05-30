from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from posts.views import AllPostView, CreatePostView
from socialmedia.views import HomeView


app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", AllPostView.as_view(), name="allposts"),
    path("create/", CreatePostView.as_view(), name="create"),
    # path("like_post/<int:post_id>/", views.like_post, name="like_post"),  # url pattern for like_post view, function like_post_view
    ]
