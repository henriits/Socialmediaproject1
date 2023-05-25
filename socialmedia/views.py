from django.contrib.auth.models import User

from posts.models import Post
from django.urls import reverse_lazy
from django.views.generic import ListView




class HomeView(ListView):
    model = Post
    template_name = "home.html"
    success_url = reverse_lazy("home")
    context_object_name = "posts"


