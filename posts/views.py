import requests
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView

from notifications.models import Notification
from .forms import CreateNewPost, CreateCommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comments, CommentLike
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.http import JsonResponse


@login_required(login_url='/login/')
def post_view(request):
    """
    This function-based view is responsible for displaying posts on the feed.
    It handles creating new posts, creating comments, and rendering the feed template.
    """

    template_name = "feed/posts.html"
    form = CreateNewPost()
    comment_form = CreateCommentForm()
    user = request.user

    quote, author = fetch_quote()
    location = user.profile.location
    weather_data = get_weather(location)

    posts = Post.objects.all().order_by("-created_date")
    post_count = Post.objects.filter(author=user).count()
    like_count = Post.objects.filter(author=user).aggregate(total_likes=Count('likes')).get('total_likes', 0)

    if request.method == 'POST':
        if 'post_id' not in request.POST:
            # Create a new post
            form = CreateNewPost(request.POST, request.FILES)
            post = create_post(request, form)
            if post:
                return redirect('posts:posts')
        else:
            # Create a new comment on a post
            comment_form = CreateCommentForm(request.POST)
            comment = create_comment(request, comment_form)
            if comment:
                return redirect('posts:posts')

    context = {
        'form': form,
        'posts': posts,
        'comment_form': comment_form,
        'post_count': post_count,
        'like_count': like_count,
        'quote': quote,
        'author': author,
        'weather_data': weather_data,
    }
    return render(request, template_name, context)


def fetch_quote():
    """
    This function fetches a random quote from an API.
    It returns the quote and the author as a tuple.
    """

    response = requests.get('https://zenquotes.io/api/random')
    quote_data = response.json()
    quote = quote_data[0]['q']
    author = quote_data[0]['a']
    return quote, author


def create_post(request, form):
    """
    This function creates a new post based on the submitted form data.
    It associates the post with the current user, saves it, and creates notifications for other users.
    It returns the created post object.
    """

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.created_date = timezone.now()
        post.save()

        users = User.objects.exclude(id=request.user.id)
        for user in users:
            notification = Notification.objects.create(
                notification_type=1,
                from_user=request.user,
                to_user=user,
                post=post
            )

        return post


def create_comment(request, comment_form):
    """
    This function creates a new comment on a post based on the submitted form data.
    It associates the comment with the current user, the corresponding post, and saves it.
    It also creates notifications for other users.
    It returns the created comment object.
    """

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        comment.post = post
        comment.user = request.user
        comment.created_at = timezone.now()
        comment.save()


        notification = Notification.objects.create(
            notification_type=2,
            from_user=request.user,
            to_user=post.author,
            post=post
        )

        return comment


def get_weather(location):
    """
    This function retrieves weather data for a given location using an external weather API.
    It returns the weather data as a dictionary.
    """

    api_key = '19ff05d2e9ea1a4230560400f04409ff'  # Replace with your OpenWeatherMap API key
    if location is None:
        location = 'Tallinn'  # Default location is set to Tallinn
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None


class PostDetailView(DetailView):
    """
    This class-based view displays a detailed view of a post, including comments and likes.
    It allows users to respond to comments from the same view.
    """

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


def total_posts(request):
    """
    This function displays the total number of posts on the sidebar.
    """

    count_posts = Post.objects.count()
    context = {'total_posts': count_posts}
    return render(request, 'sidebar.html', context)


@login_required
def like_view(request, pk):
    """
    This function handles the like/unlike functionality for a post.
    It allows users to like or unlike a post and sends appropriate notifications.
    It returns a JSON response indicating the current like status and like count.
    """

    post = get_object_or_404(Post, pk=pk)

    # Create notification for the post author
    notification = Notification.objects.create(
        notification_type=3,
        from_user=request.user,
        to_user=post.author,
        post=post
    )

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            if post.likes.filter(id=request.user.id).exists():
                # Unlike the post
                post.likes.remove(request.user)
                liked = False
            else:
                # Like the post
                post.likes.add(request.user)
                liked = True

            like_count = post.likes.count()

            return JsonResponse({'liked': liked, 'like_count': like_count})
        else:
            return JsonResponse({}, status=401)
    else:
        return JsonResponse({}, status=400)


@login_required
def comment_like_view(request, comment_id):
    """
    This function handles liking a comment.
    It allows users to like or unlike a comment on a post.
    """

    comment = get_object_or_404(Comments, id=comment_id)
    user = request.user

    if CommentLike.objects.filter(comment=comment, user=user).exists():
        # If user already liked the comment, then remove the like
        CommentLike.objects.filter(comment=comment, user=user).delete()
    else:
        # If user hasn't liked the comment, add like
        CommentLike.objects.create(comment=comment, user=user)

    return redirect('posts:posts')


class PostDeleteView(DeleteView, LoginRequiredMixin):
    """
    This class-based view allows the user to delete their own post.
    Only the post author can delete a post.
    """

    model = Post
    template_name = 'feed/post_delete.html'
    success_url = reverse_lazy('posts:posts')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the user is the owner of the post
        if self.object.author != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    This class-based view allows the comment author to delete their own comment.
    Only the comment author can delete a comment.
    """

    model = Comments
    template_name = 'feed/delete_comment.html'
    success_url = reverse_lazy('posts:posts')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


class PostUpdateView(UpdateView):
    """
    This class-based view allows the user to update their own post.
    Only the post author can update a post.
    """

    model = Post
    form_class = CreateNewPost
    template_name = 'feed/update_post.html'
    success_url = reverse_lazy('posts:posts')


def liked_users_view(request, post_id):
    """
    This function displays all the users who have liked a post.
    """

    post = get_object_or_404(Post, pk=post_id)
    liked_users = post.likes.all()

    context = {
        'post': post,
        'liked_users': liked_users
    }

    return render(request, 'feed/liked_users.html', context)
