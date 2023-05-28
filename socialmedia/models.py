# class User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE) # if user is deleted = profile deleted as well
#     image = models.ImageField(default='default_profile_pic.png', upload_to='profile_pics')
#
#     def __str__(self):
#         return f'{self.user.username} Profile'
#
# class Post(models.Model):
#     author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     image = models.ImageField(upload_to='img', blank=True, null=True)
#     text = models.CharField(max_length=250)
#     created_date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.title
#
# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     post_id = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Like(models.Model):
#     like_id = models.AutoField(primary_key=True)
#     post_id = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         if self.post:
#             return f"{self.user.username} likes post: {self.post}"
#         elif self.comment:
#             return f"{self.user.username} likes comment: {self.comment}"
#         else:
#             return "Invalid like"
#
#
#
# class Notification(models.Model):
#     notification_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     notification_type = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#
#
# class Follower(models.Model):
#     follower_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
#     follower_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)