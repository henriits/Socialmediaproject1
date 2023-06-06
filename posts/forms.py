from django import forms
from .models import Post, Comments


class CreateNewPost(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your text here!"}),
        required=True,
    )

    class Meta:
        model = Post
        fields = ['text', 'image']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
