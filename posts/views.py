from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification
from .forms import CreateNewPost, CreateCommentForm
from .models import Post, Comments
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


# Create your views here.
class AllPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "feed/posts.html"
    success_url = reverse_lazy("posts")
    context_object_name = "posts"
    ordering = ["-created_date"]  # ordering posts in descending order
    paginate_by = 10 # shows 10 posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context["posts"]
        context["comments"] = Comments.objects.filter(post_id__in=posts)
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query))  # this currently finds post text, need to fix so finds user instead
        return queryset


class CreatePostView(CreateView):
    model = Post
    form_class = CreateNewPost
    template_name = "feed/post.html"
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

    def get_template_names(self):
        return [self.template_name]



class PostDetailView(DetailView):
    model = Post
    template_name = 'feed/posts.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['comments'] = post.comments_set.all()
        context['form'] = CreateCommentForm()
        context['total_likes'] = total_likes
        return context


class CreateCommentView(CreateView):
    model = Comments
    form_class = CreateCommentForm
    template_name = 'feed/create_comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.post_id = post
        comment.user_id = self.request.user
        comment.save()
        return super().form_valid(form)

    success_url = reverse_lazy('posts:allposts')

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts:allposts'))

