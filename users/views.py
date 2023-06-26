import requests
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from posts.models import Post
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Profile


def login(request):
    """
    Handle user login.

    If the request method is POST, validate the login form and authenticate the user.
    If the user is authenticated and active, log in the user and redirect to the home page.
    If the form is not valid, display the form errors.
    If the request method is GET, display the login form.

    """
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
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    """
    Handle user registration.

    If the request method is POST, validate the registration form and create a new user account.
    If the form is valid, save the user account and display a success message.
    If the form is not valid, display the form errors.
    If the request method is GET, display the registration form.

    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            # Add a print statement to check if this line is reached
            print('Redirecting to the login page...')

            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(View):
    """

    Retrieve the user's profile and associated data such as posts, post count, and like count.
    Render the profile template with the retrieved data.

    """
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
    """
    Log out the currently authenticated user and redirect to the home page.
    """
    auth.logout(request)
    return redirect('posts:home')


def edit_profile(request):
    """
    Handle editing user profile.

    If the request method is POST, validate the profile update form and save the updated profile data.
    If the form is valid, redirect to the user's profile page.
    If the form is not valid, display the form errors.
    If the request method is GET, display the profile update form.

    """
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
    """
    Retrieve weather data for the specified location using the OpenWeatherMap API.
    return The weather data as a JSON object or None if an error occurs.
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


class UserSearch(View):
    """
    View class for searching user profiles.

    Retrieve the search query from the request GET parameters.
    Perform a case-insensitive search for profiles matching the query.
    Retrieve additional data such as post count, like count, quote, author, and weather data.
    Render the search results template with the retrieved data.

    Template: users/search.html
    """
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
    """
    Display the profile of a specific user.

    Retrieve the user object and associated posts.
    Render the profile template with the retrieved data.

    """
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user)
    return render(request, 'users/profile.html', {'user': user, 'posts': posts})
