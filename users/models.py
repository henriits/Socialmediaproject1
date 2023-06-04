from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
import os


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,primary_key="True", on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    first_name = models.CharField(max_length=30, null=False, default='John')
    last_name = models.CharField(max_length=36, null=False, default='Appleseed')
    date_of_birth = models.DateField(default='1900-01-01')
    bio = models.TextField(blank=True)
    email = models.EmailField(default='johnappleseed@example.com')

    def __str__(self):
        return f'{self.user.username} Profile'

    # to resize uploading images
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if self.image.name != old_profile.image.name:
                    # New image uploaded, delete the previous image
                    if old_profile.image.name != 'default_profile_pic.png':
                        os.remove(old_profile.image.path)
            except Profile.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

        # square box by cropping the image
        size = (300, 300)
        img = ImageOps.fit(img, size, Image.ANTIALIAS)

        img.save(self.image.path)