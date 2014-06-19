$(function() {
    // In the beginning, check if any English field has any value and
    // set the font accordingly.
    $('.english-field input').each(function(){
	if($(this).val().length == 0){
	    $(this).addClass('dinnar-light');
	}else{
	    $(this).removeClass('dinnar-light');
	}
    });
    // Watch the input fields for any changes and set the font
    // accordingly.
    $('.english-field input').on('keypress keyup',function(){
        if($(this).val().length == 0){
            $(this).addClass('dinnar-light');
        }else{
            $(this).removeClass('dinnar-light');
        }
    });
});
