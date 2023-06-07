from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from datetime import datetime
from .models import Profile


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
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'date_of_birth', 'bio', 'email', 'location']



