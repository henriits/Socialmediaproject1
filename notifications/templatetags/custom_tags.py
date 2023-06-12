from django import template

from ..models import Notification

register = template.Library()


@register.inclusion_tag('show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    unseen_notifications = Notification.objects.filter(to_user=request_user, user_has_seen=False).order_by('-date')
    count = unseen_notifications.count()
    return {'notifications': unseen_notifications, 'count': count}
