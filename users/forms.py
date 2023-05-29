# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
#
#
# class UserRegisterForm(UserCreationForm):
#
#     # def __init__(self, *args, **kwargs):
#     #     super(UserRegisterForm, self).__init__(*args, **kwargs)
#     #     # adding one class for all fields ('class': "form-control py-4")
#     #     # for field_name, field in self.fields.items():
#     #     #     field.widget.attrs['class'] = "form-control py-4"
#
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First name'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
#     email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
#
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
#


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
            'placeholder': ('Username')
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'First name',
            'type': 'first_name',
            'placeholder': ('First Name')
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'Last name',
            'type': 'last_name',
            'placeholder': ('Last Name')
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'name': 'Email',
            'type': 'email',
            'placeholder': ('Email')
        }
    ))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
            'name': 'Password',
            'type': 'password',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
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


