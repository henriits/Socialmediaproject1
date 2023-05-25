from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # if user is deleted = profile deleted as well
    image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'