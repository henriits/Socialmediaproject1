from django.db import models
from django.utils import timezone


# Create your models here.
from sorl.thumbnail import ImageField


class Post(models.Model):
    #author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    text = models.CharField(max_length=250)
    #created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
