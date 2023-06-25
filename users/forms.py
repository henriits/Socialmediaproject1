from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from datetime import datetime
from .models import Profile


class UserLoginForm(AuthenticationForm):
    """
    Form for user login.

    Inherits from AuthenticationForm, a built-in Django form for user authentication.
    Provides customizations for the username and password fields, including placeholder text.

    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.

    Inherits from UserCreationForm, a built-in Django form for user registration.
    Provides customizations for the username and password fields, including placeholder text and label.

    Template: users/register.html
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Repeat Password'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}),
        }

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'Username',
            'placeholder': 'Username'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'name': 'Password',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'name': 'Repeat password',
            'placeholder': 'Repeat Password'
        }
    ))


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile.

    Inherits from ModelForm, a built-in Django form for model-based forms.
    Defines the fields to be included in the form for updating the Profile model.
    Provides customization for the date_of_birth field with a date picker widget.

    Template: users/edit_profile.html
    """
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'date_of_birth', 'bio', 'email', 'location']
