from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import AllPostView, CreateCommentView, PostDetailView, like_view, post_view, PostDeleteView, PostUpdateView, \
    comment_like_view, LikeListView, DeleteCommentView, total_posts, liked_users_view
from socialmedia.views import HomeView


app_name = "posts"


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", post_view, name="posts"),
   # path("create/", PostView.as_view(), name="create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/create_comment/', CreateCommentView.as_view(), name='create_comment'),
    #path("comment/<int:post_id>/", CreateCommentView.as_view(), name="create_comment"),
    path("like/<int:pk>/", like_view, name="like_post"),
   # path('create_post/', PostView.as_view(), name='create_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('reply_comment/<int:post_id>', CreateCommentView.as_view(), name='reply_comment'),
    path('like/comment/<int:comment_id>/', comment_like_view, name='comment_like'),
    path('likes/<int:pk', LikeListView.as_view(), name='likes'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('liked_users/<int:post_id>', liked_users_view, name='liked_users'),
    #path('total_posts', total_posts, name='total_posts'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
