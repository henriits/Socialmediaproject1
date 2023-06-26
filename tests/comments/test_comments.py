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
