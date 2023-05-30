from django.db.models import Q
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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query))  # this currently finds post text, need to fix so finds user instead
        return queryset


class CreatePostView(CreateView):
    model = Post
    form_class = CreateNewPost
    template_name = "feed/create_post.html"
    success_url = reverse_lazy("posts:allposts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.created_date = timezone.now()
        post.save()
        return super().form_valid(form)