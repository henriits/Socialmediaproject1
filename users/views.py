import requests
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from posts.models import Post  # why this gives error?
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

def login(request):
    #
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('posts:home')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            # Add a print statement to check if this line is reached
            print('Redirecting to login page...')

            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#     # form = UserUpdateForm(instance=request.user)
#     # context = {'form': form}
#     return render(request, 'users/profile.html')
#

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = user.post_set.all().order_by('-created_date')
        post_count = Post.objects.filter(author=user).count()
        like_count = Post.objects.filter(author=user).aggregate(total_likes=Count('likes')).get('total_likes', 0)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'post_count': post_count,
            'like_count': like_count,
        }

        return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('posts:home')


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile', kwargs={'pk': profile.pk}))
        else:
            print(form.errors)  # Print the form errors for debugging
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


def get_weather(location):
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


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        post_count = Post.objects.filter(author=user).count()
        like_count = Post.objects.filter(author=user).aggregate(total_likes=Count('likes')).get('total_likes', 0)
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query)
        )

        response = requests.get('https://zenquotes.io/api/random')
        quote_data = response.json()
        quote = quote_data[0]['q']
        author = quote_data[0]['a']

        location = user.profile.location
        weather_data = get_weather(location)

        context = {
            'profile_list': profile_list,
            'post_count': post_count,
            'like_count': like_count,
            'quote': quote,
            'author': author,
            'weather_data': weather_data,
        }

        return render(request, 'users/search.html', context)


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user)
    return render(request, 'users/profile.html', {'user': user, 'posts': posts})
