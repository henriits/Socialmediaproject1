from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from posts.views import AllPostView
from socialmedia.views import HomeView


app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", AllPostView.as_view(), name="allposts")
]