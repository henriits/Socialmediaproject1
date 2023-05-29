from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import auth

# Create your views here.

def login(request):
    #
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            # if the user is in our system and if he is active, then:
            if user and user.is_active:
                # then authorize him
                auth.login(request, user)
                return HttpResponseRedirect(reverse('posts'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    # get request:
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
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

