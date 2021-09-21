$(document).ready(function(){
    $('#search_type_onsite_btn').on('click',function(){
        $('#search_type_phone_btn').removeClass('bg-custom opt-selected');
        // $('#search_type_phone_btn').addClass('text-white');
        $(this).addClass('bg-custom opt-selected');
   
        $('#search_type_phone_box').fadeOut('fast',function(){
           $('#search_type_onsite_box').fadeIn('fast');
        });
        
    })
    $('#search_type_phone_btn').on('click',function(){
       $('#search_type_onsite_btn').removeClass('bg-custom opt-selected');
      //  $('#search_type_onsite_btn').addClass('text-white');
       $(this).addClass('bg-custom opt-selected');
   
       $('#search_type_onsite_box').fadeOut('fast',function(){
           $('#search_type_phone_box').fadeIn('fast');
       });
   })
   $('.search_btn').on('click',function(){
     $(this).addClass('loading');
   });       
       $('.ui.dropdown')
       .dropdown({
         apiSettings: {
           // this url parses query server side and returns filtered results
           url: '//api.semantic-ui.com/tags/{query}'
         },
       })
     ;
     
     $('.search-prop-header').on('click',function(){
       const id = '#' + $(this).attr('data-value');
       $(id).slideToggle();
       $(this).find('.open-icon i').toggleClass('rotate');
     })
})