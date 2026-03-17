console.log("script.js loaded, jQuery:", typeof $);

$(document).ready(function () {
    
    $("#add-book").submit(function(e) {
    e.preventDefault();

    alert("INTERCEPTED")

    // var form = $(this);
    // var actionURL = form.attr('action');

    // $.ajax({
    //     type: 'POST',
    //     url: actionURL,
    //     data: new FormData(this),
    //     processData: false,
    //     contentType: false,

    //     success: function(response)
    //     {
    //         if (response.success) {
    //             $("#response").text(response.message);
    //         } else {
    //             console.log(response.errors);
    //         }
    //     }
    // });
});
});