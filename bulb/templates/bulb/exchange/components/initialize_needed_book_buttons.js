function initialize_needed_book_buttons(){
    $(".edit-needed-book").click(function () {
        // show the edit book modal {# you can find it in bulb/exchange/home.html #}
        $("#edit-needed-book-modal").modal('show');
        var url = $(this).data('url'); 

        $("#edit-needed-book-modal .modal-title").html("عدّل طلب كتاب");
        $("#edit-needed-book-modal .modal-body").load(url);

        var $submitButton = $("#edit-needed-book-modal button.submit-button");
        // Unbind any handlers previously attached to the submit button
        // This is necessary to avoid multiple submissions of the form
        $submitButton.off('click');
        $submitButton.click(function () {
            $("form#edit-needed-book-form").submit();
        });
    });
    $("button.confirm-delete-needed-book").click(function(){
        var confirm_url = $(this).data('confirm-url');
        var deletion_url = $(this).data('deletion-url');
        $('#confirm-delete-needed-book-modal .modal-body').load(confirm_url);
        $("#delete-book").data('deletion-url', deletion_url); 
        $("#confirm-delete-needed-book-modal").modal('show');
    });
}