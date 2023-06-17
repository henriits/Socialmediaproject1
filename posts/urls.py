from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PostDetailView, like_view, post_view, PostDeleteView, PostUpdateView, \
    comment_like_view, LikeListView, DeleteCommentView, liked_users_view
from socialmedia.views import HomeView


app_name = "posts"


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", post_view, name="posts"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path("like/<int:pk>/", like_view, name="like_post"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('like/comment/<int:comment_id>/', comment_like_view, name='comment_like'),
    path('likes/<int:pk', LikeListView.as_view(), name='likes'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('liked_users/<int:post_id>', liked_users_view, name='liked_users'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
