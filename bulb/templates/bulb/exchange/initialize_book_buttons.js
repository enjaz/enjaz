function initialize_book_buttons(){
    $(".order-book").click(function () {
        $("#order-book-modal").modal('show');
        var pk = $(this).data('pk');
        $("#order-book-modal .modal-body").load("{% url 'bulb:order_instructions' %}", {pk: pk});

        var $submitButton = $("#order-book-modal button.submit-button");
        // Unbind any handlers previously attached to the submit button
        // This is necessary to avoid multiple submissions of the form
        $submitButton.off('click');
        $submitButton.click(function () {
            $("form#order-book-form").submit();
            loadBooks();
        });
    });
    $(".edit-book").click(function () {
        var pk = $(this).data('pk');
        // show the edit book modal {# you can find it in bulb/exchange/home.html #}
        $("#edit-book-modal").modal('show');
        var url = $(this).data('url'); 

        $("#edit-book-modal .modal-title").html("عدّل كتاب");
        $("#edit-book-modal .modal-body").load(url);

        var $submitButton = $("#edit-book-modal button.submit-button");
        // Unbind any handlers previously attached to the submit button
        // This is necessary to avoid multiple submissions of the form
        $submitButton.off('click');
        $submitButton.click(function () {
            $("form#edit-book-form").submit();
        });
    });
    $("button.confirm-delete-book").click(function(){
        console.log(0);
        var confirm_url = $(this).data('confirm-url');
        var deletion_url = $(this).data('deletion-url');
        $('#confirm-delete-book-modal .modal-body').load(confirm_url);
        $("#delete-book").data('deletion-url', deletion_url); 
        $("#confirm-delete-book-modal").modal('show');
    });
}