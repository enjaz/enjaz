function initialize_session_buttons(){
    $(".confirm-attend-session, .confirm-cancel-session").click(function(){
        var action = $(this).data('action');
        var pk = $(this).data('pk');
        $("#confirm-" + action + "-session-modal").modal('show');
        $("#" + action + "-session").data('pk', pk);
    });
    $("#attend-session, #cancel-session").click(function () {
        var pk = $(this).data('pk');
        var action = $(this).data('action');
        $.ajax({
            url: "{% url 'bulb:toggle_session_confirmation' %}",
            type: 'POST',
            data: {session_pk: pk, action: action},
            cache: false,
            success: function (data) {
                if (data.message == "success") {
                    // show success message (using toastr)
                    toastr.options.positionClass = "toast-top-left";
                    if (action == 'join'){
                        toastr.success("أُكد الحضور");
                    } else if (action == 'leave') {
                        toastr.success("أُلغي تأكيد الحضور");
                    }
                    $("#confirm-" + action + "-session-modal").modal('hide');
                    $("#confirm-" + action + "-session-modal").on('hidden.bs.modal', function(){
                        window.location.href = data.show_url;
                    });
                } else {
                    toastr.error(data.message);
                }
            }
        });
    });
}