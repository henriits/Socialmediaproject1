from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import AllPostView, CreatePostView, CreateCommentView, PostDetailView, LikeView
from socialmedia.views import HomeView


app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", AllPostView.as_view(), name="allposts"),
    path("create/", CreatePostView.as_view(), name="create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/create_comment/', CreateCommentView.as_view(), name='create_comment'),
    #path("comment/<int:post_id>/", CreateCommentView.as_view(), name="create_comment"),
    path("like/<int:pk>/", LikeView, name="like_post"),
]

