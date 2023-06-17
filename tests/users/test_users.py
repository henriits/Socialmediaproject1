import pytest
from django.contrib.auth.models import User
from PIL import Image
from users.models import Profile



@pytest.mark.django_db
def test_new_register_user_not_superuser():
    user = User.objects.create_user('newuser', is_superuser=False)

    assert user.is_superuser == False

@pytest.mark.django_db
def test_profile_default_image():
    user = User.objects.create(username='testuser')
    profile = Profile.objects.create(user=user)

    assert profile.image.name == 'default_profile_pic.png'