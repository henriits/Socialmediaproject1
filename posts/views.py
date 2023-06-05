
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification
from .forms import CreateNewPost, CreateCommentForm
from .models import Post, Comments
from django.contrib.auth.mixins import LoginRequiredMixin
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


def post_view(request):
    template_name = "feed/posts.html"
    form = CreateNewPost()
    comment_form = CreateCommentForm()
    posts = Post.objects.all().order_by("-created_date")
    if request.method == 'POST':
        if 'post_id' not in request.POST:
            form = CreateNewPost(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.instance.created_date = timezone.now()
                form.save()

                return redirect('posts:posts')

        else:
            comment_form = CreateCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')  # Assuming 'post_id' is the name of the input field in the form
                post = Post.objects.get(pk=post_id)
                comment.post = post
                comment.user = request.user
                comment.created_at = timezone.now()
                comment.save()

                return redirect('posts:posts')

    context = {
        'form': form,
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, template_name, context)


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

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('posts:posts'))


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'feed/post_delete.html'
    success_url = reverse_lazy('posts:posts')


class PostUpdateView(UpdateView):
    model = Post
    form_class = CreateNewPost
    template_name = 'feed/update_post.html'
    success_url = reverse_lazy('posts:posts')
