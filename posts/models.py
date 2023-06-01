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
    text = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post_id.title} - {self.user_id.username}'


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.post:
            return f"{self.user.username} likes post: {self.post}"
        elif self.comment:
            return f"{self.user.username} likes comment: {self.comment}"
        else:
            return "Invalid like"