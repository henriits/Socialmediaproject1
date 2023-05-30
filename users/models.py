from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')
    first_name = models.CharField(max_length=30, null=False, default='John')
    last_name = models.CharField(max_length=36, null=False, default='Appleseed')
    date_of_birth = models.DateField(default='1900-01-01')
    bio = models.TextField(blank=True)
    email = models.EmailField(default='johnappleseed@example.com')

    def __str__(self):
        return f'{self.user.username} Profile'
