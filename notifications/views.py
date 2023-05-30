from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user_id=user, is_read=False)

    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(notification_id=notification_id)
        notification.is_read = True
        notification.save()
        return redirect('notifications')

    return render(request, 'notifications.html', {'notifications': notifications})
