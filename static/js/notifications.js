function showNotifications() {
    const container = document.getElementById('notification-container');

    if (container.classList.contains('d-none')) {
        container.classList.remove('d-none');
        updateNotificationCount(0); // Mark all notifications as seen
    } else {
        container.classList.add('d-none');
    }
}
