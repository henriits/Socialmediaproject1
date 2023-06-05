from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

import users
from notifications.models import Notification
from posts.models import Post


class PostNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('post-detail', pk=object_pk)
class FollowNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = User.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('profile', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')