from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from posts.models import Post, Comments

class Notification(models.Model):
    # notification_type choices
    NEW_POST = 1
    COMMENT = 2
    LIKE = 3
    MESSAGE = 4

    NOTIFICATION_TYPES = (
        (NEW_POST, 'New Post'),
        (COMMENT, 'Comment'),
        (LIKE, 'Like'),
        (MESSAGE, 'Message'),
    )

    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the notification is for a new post and if the creator is the same as the post's author
        if self.notification_type == self.NEW_POST and self.to_user == self.post.author:
            return  # Don't save the notification

        # Check if the notification is for commenting on a post and if the commenter is the same as the post's author
        if self.notification_type == self.COMMENT and self.from_user == self.post.author:
            return  # Don't save the notification

        # Check if the notification is for liking a post and if the liker is the same as the post's author
        if self.notification_type == self.LIKE and self.from_user == self.post.author:
            return  # Don't save the notification

        # Check if the notification is for sending a message and if the sender is the same as the recipient
        if self.notification_type == self.MESSAGE and self.from_user == self.to_user:
            return  # Don't save the notification

        super().save(*args, **kwargs)

