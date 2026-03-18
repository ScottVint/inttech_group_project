$(document).ready(function () {
    
    $(".dropdown-menu").on("submit", ".add-to-reading", function(e) {
    e.preventDefault();

    var form = $(this);
    var actionURL = form.attr('action');
    var button = form.closest(".dropdown").find("button.button_two").first()

    $.ajax({
        type: 'POST',
        url: actionURL,
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function(response)
        {
            if (response.success) {
                $("#response").text(response.message);
                button.prop("disabled", true);
                button.html('Reading')
                button.addClass("added")

            } else {
                console.log(response.errors);
            }
        }
    });

});
  $(".dropdown-menu").on("submit", ".add-to-wishlist", function(e) {
    e.preventDefault();

    var form = $(this);
    var actionURL = form.attr('action');
    var button = form.closest(".dropdown").find("button.button_two").first()

    $.ajax({
        type: 'POST',
        url: actionURL,
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function(response)
        {
            if (response.success) {
                $("#response").text(response.message);
                button.html('Wishlisted')
                button.addClass("wishlisted")

            } else {
                console.log(response.errors);
            }
        }
    });

});
});