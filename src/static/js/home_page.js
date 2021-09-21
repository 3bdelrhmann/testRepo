$(document).ready(function(){
 $('#search_type_onsite_btn').on('click',function(){
     $('#search_type_phone_btn').removeClass('bg-white opt-selected');
     $('#search_type_phone_btn').addClass('text-white');
     $(this).addClass('bg-white opt-selected');

     $('#search_type_phone_box').fadeOut('fast',function(){
        $('#search_type_onsite_box').fadeIn('fast');
     });
     
 })
 $('#search_type_phone_btn').on('click',function(){
    $('#search_type_onsite_btn').removeClass('bg-white opt-selected');
    $('#search_type_onsite_btn').addClass('text-white');
    $(this).addClass('bg-white opt-selected');

    $('#search_type_onsite_box').fadeOut('fast',function(){
        $('#search_type_phone_box').fadeIn('fast');
    });
})
$('.search_btn').on('click',function(){
  $(this).addClass('loading');
});
    
    // function toggle_book(){

    // }
    // $('.change_book').on('click',function(){
    //     const id = '#' + $(this).attr('id');

    // })

    $('.ui.dropdown')
    .dropdown({
      apiSettings: {
        // this url parses query server side and returns filtered results
        url: '//api.semantic-ui.com/tags/{query}'
      },
    })
  ;
  
})