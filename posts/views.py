from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import CreateNewPost
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class AllPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "feed/posts.html"
    success_url = reverse_lazy("posts")
    context_object_name = "posts"


class CreatePostView(CreateView):
    model = Post
    form_class = CreateNewPost
    template_name = "templates/create_post.html"
    success_url = reverse_lazy("create")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.created_date = timezone.now()
        post.save()
        return redirect('posts')
