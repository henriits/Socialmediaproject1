from django.db import models

# Create your models here.
from sorl.thumbnail import ImageField


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.title
