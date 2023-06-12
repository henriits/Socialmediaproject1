function showNotifications() {
    const container = document.getElementById('notification-container');

    if (container.classList.contains('d-none')) {
        container.classList.remove('d-none');
        updateNotificationCount(0); // Mark all notifications as seen
    } else {
        container.classList.add('d-none');
    }
}

function removeNotification(notificationId, element, redirectURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            if (xmlhttp.status == 200) {
                removeNotificationElement(element); // Remove the notification from the dropdown
                updateNotificationCount(-1); // Decrease the notification count by 1

                if (redirectURL) {
                    window.location.href = redirectURL; // Redirect to the notification origin
                }
            } else {
                alert('There was an error: ' + xmlhttp.responseText); // Display the error message
            }
        }
    };

    xmlhttp.open("DELETE", `/notifications/remove/${notificationId}/`, true); // Update the URL with the correct endpoint
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xmlhttp.send();
}

function updateNotificationCount(change) {
    const notificationCount = document.getElementById('notification-count');
    if (notificationCount) {
        const count = parseInt(notificationCount.textContent);
        const updatedCount = count + change;
        if (updatedCount <= 0) {
            notificationCount.remove(); // Remove the notification count badge if it becomes zero or negative
        } else {
            notificationCount.textContent = updatedCount;
        }
    }
}

function removeNotificationElement(element) {
    var parent = element.parentNode;
    parent.parentNode.removeChild(parent);
}
