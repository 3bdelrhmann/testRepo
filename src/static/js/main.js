

$(document).ready(function() {
    $('#close-btn').on('click',function(){
        $('.overlay-menu').css('left','100%');
    });
    $('#menu-btn').on('click',function(){
        $('.overlay-menu').css('left','0');
    });
    $('.open_options').on('click',function(){
        $('#options_list').slideToggle();
    })

});
