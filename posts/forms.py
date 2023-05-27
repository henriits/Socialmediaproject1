from django import forms
from .models import Post

class CreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', ]