from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import AllPostView, CreatePostView, create_comment
from socialmedia.views import HomeView


app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", AllPostView.as_view(), name="allposts"),
    path("create/", CreatePostView.as_view(), name="create"),
    path("comment/<int:post_id>/", create_comment, name="create_comment"),
    # path("like_post/<int:post_id>/", views.like_post, name="like_post"),  # url pattern for like_post view, function like_post_view
]

