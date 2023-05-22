from django.contrib.auth.models import User

from posts.models import Post
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from socialmedia.forms import SignUpForm


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    success_url = reverse_lazy("home")
    context_object_name = "posts"



class UserCreateView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)