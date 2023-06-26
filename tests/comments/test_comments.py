import pytest
from django.contrib.auth.models import User

from posts.models import Post, Comments


@pytest.mark.django_db
def test_comments():
    # Preparation phase
    user = User.objects.create_user(username='testuser')
    post = Post.objects.create(title='My new post', author=user)
    comment = Comments.objects.create(comment='My comment', user=user, post=post)

    # Assertion
    assert comment.comment == 'My comment'
    assert comment.user == user
    assert comment.post == post

@pytest.mark.django_db
def test_add_comment():
    # Create a user for the post author
    author = User.objects.create_user(username='testuser', password='testpassword')
    # Create a post
    post = Post.objects.create(author=author, title='Test Post', text='This is a test post.')
    # Create a user for commenting on the post
    user = User.objects.create_user(username='commenter', password='commenterpassword')
    comment_text = 'This is a test comment.'

    # Add a comment to the post
    comment = Comments.objects.create(post=post, user=user, comment=comment_text)
    assert post.comments.count() == 1
    assert comment.post == post
    assert comment.user == user
    assert comment.comment == comment_text
