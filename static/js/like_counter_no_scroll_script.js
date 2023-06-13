<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function() {
  // Get the CSRF token from the cookie
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $('.like-button').on('click', function(event) {
    event.preventDefault();  // Prevent the default button behavior

    var button = $(this);  // Store the button element
    var countElement = $(button.data('count-element'));  // Get the associated like count element using the data attribute

    var postId = button.data('post-id');  // Get the post ID from the data attribute

    // Get the CSRF token
    var csrftoken = getCookie('csrftoken');

    // Send an AJAX POST request to the server
    $.ajax({
      type: 'POST',
      url: '/like/' + postId + '/',
      data: {
        'post_id': postId  // Pass the post ID in the data
      },
      headers: {
        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
      },
      success: function(response) {
        // Handle the successful response
        if (response.liked) {
          button.text('Unlike');  // Change the button text to Unlike
          countElement.text(response.like_count); // Update the like count element
        } else {
          button.text('Like');  // Change the button text to Like
          countElement.text(response.like_count); // Update the like count element
        }
      },
      error: function(xhr) {
        // Handle any errors that occur during the AJAX request
      }
    });
  });
});


</script>