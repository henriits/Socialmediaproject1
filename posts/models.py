from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
from sorl.thumbnail import ImageField


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # here is a many to one relationship, need to explain is here "auth.User" or User?
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='img', blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.text


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post_id.title} - {self.user_id.username}'

