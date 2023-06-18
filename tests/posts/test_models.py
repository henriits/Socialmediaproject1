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

@pytest.mark.django_db
def test_post_creation():
    # Create a user for the post author
    author = User.objects.create_user(username='testuser', password='testpassword')
    # Create a post
    post = Post.objects.create(author=author, title='Test Post', text='This is a test post.')
    # Assert post properties
    assert post.author == author
    assert post.title == 'Test Post'
    assert post.text == 'This is a test post.'
    assert post.likes.count() == 0
    assert post.total_likes() == 0
    assert post.total_comments() == 0
    assert post.get_likes_count() == 0
    assert str(post) == 'This is a test post.'







