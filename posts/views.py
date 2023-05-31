from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification
from .forms import CreateNewPost, CreateCommentForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class AllPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "feed/posts.html"
    success_url = reverse_lazy("posts")
    context_object_name = "posts"
    ordering = ["-created_date"]  # ordering posts in descending order
    paginate_by = 10 # shows 10 posts per page

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

        Notification.objects.create(
            user_id=self.request.user,
            notification_type='new_post',
            content=f'A new post "{post.title}" has been created.'
        )


        return super().form_valid(form)

def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.user_id = request.user
            comment.save()
            return redirect('posts')
    else:
        form = CreateCommentForm()

    context = {
        'form': form,
    }
    return render(request, 'feed/create_comment.html', context)