function initialize_membership_buttons(){
    $(".confirm-join, .confirm-leave").click(function(){
        var action = $(this).data('action');
        var pk = $(this).data('pk');
        $("#confirm-" + action + "-modal").modal('show');
        $("#" + action + "-group").data('pk', pk);
    });
    $("#join-group, #leave-group").click(function () {
        var pk = $(this).data('pk');
        var action = $(this).data('action');
        $.ajax({
            url: "{% url 'bulb:control_membership' %}",
            type: 'POST',
            data: {group_pk: pk, action: action},
            cache: false,
            success: function (data) {
                if (data.message == "success") {
                    // show success message (using toastr)
                    toastr.options.positionClass = "toast-top-left";
                    if (action == 'join'){
                        toastr.success("انضممت للمجموعة");
                        $("#confirm-join-modal .modal-body").load("{% url 'bulb:new_member_introduction' group.pk %}")
                    } else if (action == 'leave') {
                        toastr.success("غادرت المجموعة");
                        $("#confirm-" + action + "-modal").modal('hide');
                    }
                    $("#confirm-" + action + "-modal").on('hidden.bs.modal', function(){
                        window.location.href = data.show_url;
                    });
                } else {
                    toastr.error(data.message);
                }
            }
        });
    });
}