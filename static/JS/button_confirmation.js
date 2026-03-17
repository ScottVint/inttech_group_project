console.log("script.js loaded, jQuery:", typeof $);

$(document).ready(function () {
    
    $(document).on("submit", ".add-book", (function(e) {
    e.preventDefault();

    var form = $(this);
    var actionURL = form.attr('action');

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
            } else {
                console.log(response.errors);
            }
        }
    });

}));
});