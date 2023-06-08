from django import template
from django.contrib.auth.models import User
from django.db import models
from users.models import Profile

register = template.Library()

@register.simple_tag
def get_new_users(limit=5):
    new_users = User.objects.order_by('-date_joined')[:limit]
    user_ids = [user.id for user in new_users]
    profiles = Profile.objects.filter(user_id__in=user_ids).order_by(
        models.Case(*[models.When(user_id=user_id, then=index) for index, user_id in enumerate(user_ids)])
    )
    users_with_profiles = zip(new_users, profiles)
    return users_with_profiles


