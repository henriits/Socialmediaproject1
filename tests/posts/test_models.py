import pytest
from django.contrib.auth.models import User
from posts.models import Post, Comments



@pytest.mark.django_db
def test_posts():
    # Preparation phase
    user = User.objects.create_user("foo", is_superuser= True)
    post = Post.objects.create(title="My new post", author= user)

    # Assertion

    assert post.likes == 1
    assert user.is_superuser == True
    assert user.username == "foo"
    assert post.title

@pytest.mark.django_db
def test_comment():
    # Preparation phase
    user = User.objects.create_user(username="testuser")
    post = Post.objects.create(title="My new post", author=user)
    comment = Comments.objects.create(comment="My comment", user=user, post=post)

    # Assertion
    assert comment.comment == "My comment"
    assert comment.user == user
    assert comment.post == post