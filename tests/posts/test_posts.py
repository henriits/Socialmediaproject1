import pytest
from django.contrib.auth.models import User
from posts.models import Post,Comments


@pytest.mark.django_db
def test_posts():
    # Preparation phase
    user = User.objects.create_user("foo", is_superuser=True)
    post = Post.objects.create(title="My new post", author=user)

    # Assertion
    assert post.likes.count() == 0  # Initially, there are no likes
    assert user.is_superuser is True
    assert user.username == "foo"
    assert post.title == "My new post"


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


@pytest.mark.django_db
def test_create_post():
    user = User.objects.create(username='test_user')
    post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
    assert Post.objects.count() == 1
    assert post.title == 'Test Post'
    assert post.author == user


@pytest.mark.django_db
def test_create_post():
    user = User.objects.create(username='test_user')
    post = Post.objects.create(title='Test Post', text='This is a test post.', author=user)
    assert Post.objects.count() == 1
    assert post.title == 'Test Post'
    assert post.author == user


@pytest.mark.django_db
def test_get_post():
    user = User.objects.create(username='test_user')
    post = Post.objects.create(title='Test Post', text='This is a test post.', author=user)
    retrieved_post = Post.objects.get(title='Test Post')
    assert retrieved_post == post

@pytest.mark.django_db
def test_post_creation():
    # Create a user for the post author
    author = User.objects.create_user(username='testuser', password='testpassword')
    # Create a post
    post = Post.objects.create(author=author, title='Test Post', text='Test Post')
    # Assert post properties
    assert post.author == author
    assert post.title == 'Test Post'
    assert post.text == 'Test Post'
    assert post.likes.count() == 0
    assert str(post) == 'Test Post'



@pytest.mark.django_db
def test_like_post():
    # Create a user for the post author
    author = User.objects.create_user(username='testuser', password='testpassword')
    # Create a post
    post = Post.objects.create(author=author, title='Test Post', text='This is a test post.')
    # Create users for liking the post
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')

    # User1 likes the post
    post.likes.add(user1)
    assert post.likes.count() == 1

    # User2 likes the post
    post.likes.add(user2)
    assert post.likes.count() == 2

    # User1 tries to like the post again (duplicate like)
    post.likes.add(user1)
    assert post.likes.count() == 2  # Duplicate like should be ignored


@pytest.mark.django_db
def test_unlike_post():
    # Create a user for the post author
    author = User.objects.create_user(username='testuser', password='testpassword')
    # Create a post
    post = Post.objects.create(author=author, title='Test Post', text='This is a test post.')
    # Create users for liking the post
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')

    # User1 and User2 like the post
    post.likes.add(user1, user2)
    assert post.likes.count() == 2

    # User1 unlikes the post
    post.likes.remove(user1)
    assert post.likes.count() == 1

    # User2 unlikes the post
    post.likes.remove(user2)
    assert post.likes.count() == 0