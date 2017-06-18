// If you modify the following function, you will probably also need
// to modify the one in clubs/templates/clubs/forms/form_edit.html
$(hide_choices);
$('.dynamic-form-add a').click(hide_choices);

function hide_choices(){
	$('select[id^="id_fields-"]').bind('ready change', function(){
		console.log('a');
		// define field values for which choices do not apply.
		var show_choices_fields = [5,8];
		// extract the full field id number.
		var id_number_regex = /id_fields-(\d)-field_type/;
		var id_number = id_number_regex.exec($(this).attr('id'))[1];
		// generate the choices field id
		var choice_field_id = 'id_fields-' + id_number + '-choices';
		// check if the choices field should be shown or hidden.
		if (show_choices_fields.indexOf(parseInt($(this).val())) > -1) {
			$('#' + choice_field_id).fadeIn('slow');
		} else {
			$('#' + choice_field_id).fadeOut('slow');
		}
	});
}
