from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from posts.models import Post


# Create your views here.
class PostView(ListView):
    model = Post
    template_name = "feed/posts.html"
    success_url = reverse_lazy("posts")
    context_object_name = "posts"
