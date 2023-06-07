$(document).ready(function() {
    $('.show-all-btn').click(function(e) {
        e.preventDefault();
        $('.additional-posts').slideToggle();
    });
});
