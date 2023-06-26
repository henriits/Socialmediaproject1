from django.urls import path
from .views import show_notifications

urlpatterns = [

    path('notifications/', show_notifications, name='show_notifications'),

]
