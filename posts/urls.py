from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import AllPostView,  CreateCommentView, PostDetailView, LikeView, post_view
from socialmedia.views import HomeView


app_name = "posts"


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", post_view, name="posts"),
   # path("create/", PostView.as_view(), name="create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/create_comment/', CreateCommentView.as_view(), name='create_comment'),
    #path("comment/<int:post_id>/", CreateCommentView.as_view(), name="create_comment"),
    path("like/<int:pk>/", LikeView, name="like_post"),
   # path('create_post/', PostView.as_view(), name='create_post'),
]