
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from notifications.models import Notification
from .forms import CreateNewPost, CreateCommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comments, CommentLike
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
#import pdb

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


from django.contrib.auth.models import User

def post_view(request):
    template_name = "feed/posts.html"
    form = CreateNewPost()
    comment_form = CreateCommentForm()
    posts = Post.objects.all().order_by("-created_date")
    if request.method == 'POST':
        if 'post_id' not in request.POST:
            form = CreateNewPost(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.created_date = timezone.now()
                post.save()

                # Create notifications for other users
                users = User.objects.exclude(id=request.user.id)
                for user in users:
                    notification = Notification.objects.create(
                        notification_type=1,
                        from_user=request.user,
                        to_user=user,
                        post=post
                    )

                return redirect('posts:posts')
        else:

            comment_form = CreateCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(pk=post_id)
                comment.post = post
                comment.user = request.user
                comment.created_at = timezone.now()
                comment.save()

                # Create notifications for other users
                users = User.objects.exclude(id=request.user.id)
                for user in users:
                    notification = Notification.objects.create(
                        notification_type=2,
                        from_user=request.user,
                        to_user=user,
                        post=post
                    )



    context = {
        'form': form,
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, template_name, context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'feed/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        total_likes = post.total_likes()
        context['comments'] = post.comments.all()
        context['form'] = CreateCommentForm()
        context['total_likes'] = total_likes
        return context


class CreateCommentView(CreateView, LoginRequiredMixin):
    model = Comments
    form_class = CreateCommentForm
    template_name = 'feed/create_comment.html'
    success_url = reverse_lazy('posts:posts')

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.post_id = post
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    success_url = reverse_lazy('posts:allposts')


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

        # Create notification for the post author
        notification = Notification.objects.create(
            notification_type=3,
            from_user=request.user,
            to_user=post.author,
            post=post
        )

    return HttpResponseRedirect(reverse('posts:posts'))

@login_required
def comment_like_view(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    user = request.user

    if CommentLike.objects.filter(comment=comment, user=user).exists():
        # If user already liked the comment, then remove the like
        CommentLike.objects.filter(comment=comment, user=user).delete()
    else:
        # If user hasn't liked the comment, add like
        CommentLike.objects.create(comment=comment, user=user)

    return redirect('posts:posts')


class LikeListView(ListView):
    model = Post
    template_name = 'feed/likes.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs['pk'])


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'feed/post_delete.html'
    success_url = reverse_lazy('posts:posts')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the user is the owner of the post
        if self.object.author != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(UpdateView):
    model = Post
    form_class = CreateNewPost
    template_name = 'feed/update_post.html'
    success_url = reverse_lazy('posts:posts')
