from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from datetime import datetime


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        # 'class': "form-control py-4", - moving this to def __init__
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'class': "form-control py-4",
        'placeholder': 'Enter your password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'Username',
            'type': 'username',
            'placeholder': 'Username'
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'first_name',  # Corrected attribute name
            'type': 'first_name',
            'placeholder': 'First Name'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'last_name',  # Corrected attribute name
            'type': 'last_name',
            'placeholder': 'Last Name'
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'name': 'Email',
            'type': 'email',
            'placeholder': 'Email'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'name': 'Password',
            'type': 'password',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'name': 'Repeat password',
            'placeholder': 'Repeat Password'
        }
    ))
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={
            'name': 'Date of birth',
            'type': 'date',
            'max': datetime.now().date()
        }
    ))
