from django import forms
from .models import Post, Comments

class CreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['user_id', 'comment']