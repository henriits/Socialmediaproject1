from django.db import models

# Create your models here.
from sorl.thumbnail import ImageField


class Post(models.Model):
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=250)
    image = ImageField()

    def __str__(self):
        return self.title