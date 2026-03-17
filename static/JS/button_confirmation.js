$(document).ready(function () {
    
    $(document).on("submit", ".add-book", function(e) {
    e.preventDefault();

    var form = $(this);
    var actionURL = form.attr('action');
    var button = form.find(".button_two")

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
                button.attr("disabled", true);
                button.html('Added')
                button.addClass("added")

            } else {
                console.log(response.errors);
            }
        }
    });

});
});