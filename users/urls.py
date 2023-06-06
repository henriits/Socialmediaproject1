from django.urls import path
from . import views as user_views

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>', user_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', user_views.user_profile, name='user_profile'),
]
