from django.urls import path
from .views import PostNotification, FollowNotification, RemoveNotification

urlpatterns = [
    path('notification/<int:notification_pk>/post/<int:object_pk>', PostNotification.as_view(),
         name='post-notification'),
    path('notification/<int:notification_pk>/follow/<int:object_pk>', FollowNotification.as_view(),
         name='follow-notification'),
    path('notifications/remove/<int:notification_pk>/', RemoveNotification.as_view(), name='remove_notification'),
]
