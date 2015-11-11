function initialize_book_buttons(){
    $(".order-book").click(function () {
        var instruction_url = $(this).data('instruction-url');
        $("#order-book-modal").modal('show');
        $("#order-book-modal .modal-body").load(instruction_url, function(){
            $(function(){
                direct_height = $('.order-option.direct').height();
                indirect_height = $('.order-option.indirect').height();
                if (direct_height > indirect_height){
                    $('.order-option.indirect').height(direct_height);
                }
            });

            $('.order-option').click(function() {
                order_button = this;
                var confirm_url = $(order_button).data('confirm-url');
                $("#confirm-order-modal .modal-body").load(confirm_url, function(){
                    $("#id_borrowing_end_date").attr('data-start-view', '1').datepicker({isRTL: true, minDate: 1{% if book.available_until %},maxDate: new Date({{ book.available_until.year }}, {{ book.available_until.month }} - 1, {{ book.available_until.day }}){% endif %}});
                    if ($(order_button).hasClass('direct')){
                        $("#id_delivery").val('D');
                    } else if ($(order_button).hasClass('indirect')){
                        $("#id_delivery").val('I');
                    }
                });
                $("#confirm-order-modal").modal('show');
            });
        });
    });
    $(".edit-book").click(function () {
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
        var confirm_url = $(this).data('confirm-url');
        var deletion_url = $(this).data('deletion-url');
        $('#confirm-delete-book-modal .modal-body').load(confirm_url);
        $("#delete-book").data('deletion-url', deletion_url); 
        $("#confirm-delete-book-modal").modal('show');
    });
}