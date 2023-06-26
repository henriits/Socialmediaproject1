from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def show_notifications(request):
    # Get the notifications for the authenticated user
    notifications = Notification.objects.filter(to_user=request.user)

    # Mark all notifications as seen
    notifications.update(user_has_seen=True)

    # Render the template with the notifications
    return render(request, 'show_notifications.html', {'notifications': notifications})
