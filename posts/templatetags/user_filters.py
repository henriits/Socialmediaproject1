from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter(name='time_since_registration')
def time_since_registration(value):
    duration = timesince(value.date_joined)
    return f"You have been a member for : {duration}"