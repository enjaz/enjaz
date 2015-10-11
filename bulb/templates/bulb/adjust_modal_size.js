    // ----
    // enable scrolling in modal body due to its length
    // script source: http://stackoverflow.com/a/20765540/4249696
    $(document).ready(ajustamodal);
    $(window).resize(ajustamodal);
    function ajustamodal() {
        var altura = $(window).height() - 155; //value corresponding to the modal heading + footer
        $(".ativa-scroll").css({"height":altura,"overflow-y":"auto"});
    }