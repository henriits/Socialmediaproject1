from django import forms
from .models import Post, Comments

class CreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']