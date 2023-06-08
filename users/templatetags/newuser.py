from django import template
from django.contrib.auth.models import User


register = template.Library()

@register.simple_tag
def get_new_users(limit=5):
    new_users = User.objects.order_by('-date_joined')[:limit]
    return new_users



