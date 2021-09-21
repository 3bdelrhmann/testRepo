$(document).ready(function(){
    function get_results(form_data,page_num,is_search=false){
        if(form_data){
            form_data = form_data + '&page_num=' +  page_num;
            dataSend  = form_data
        }else{
            dataSend = {
                'page_num' : page_num,
            }
        }
        var response = $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'GET',
            cache: false,
            url: assistants_search_url,
            data : dataSend,
            beforeSend: function() {
                if(is_search == true){
                    $('#clients_box').html('');
                    $('#assistant-title').fadeOut('fast',function(){
                        $('#assistant-title').text('نتائج البحث');
                        $('#assistant-title').fadeIn('fast')
                    });

                }
                $('#loading_ico').fadeIn('fast');
            },
            success: function (response, status, xhr) {
                for (let index = 0; index < response.length; index++) {
                    
                    obj_id          = response[index]['id']
                    assistant_name  = response[index]['first_name']
                    assistant_email = response[index]['email']
                    

                    assistant = $('#client_empty_box').html();
                    assistant_ = $(assistant).appendTo('#clients_box').fadeIn('slow');

                    console.log(obj_id)

                    /* DELETE ATTRS*/
                    $(assistant_).attr('data-obj-id',obj_id);
                    $(assistant_).find('#delete-object').attr('data-id-delete',obj_id);
                    /* DELETE ATTRS*/
                    $(assistant_).find('#update_assistant_url').attr('href',update_assistant_url+obj_id);


                    $(assistant_).find('#assistant_mail').html(assistant_email)
                    $(assistant_).find('#assistant_name').html(assistant_name)

                }
                if(response.length == 0){
                    if(is_search == true){
                        $('#clients_box').html('');
                    }
                    $('#load_more').attr('disabled',true);
                    $('#load_more').html('لا توجد نتائج');
                }else{
                    $('#load_more').html('تحميل المزيد');
                    $('#load_more').addClass('btn-base');
                    $('#load_more').removeClass('custom-disabled');
                    $('#load_more').attr('disabled',false);
                }
            },
            error: function (xhrObj, status, errType) {
            },
            complete: function (xhrObj, status) {
                $('#loading_ico').fadeOut();
            }
        });
    }
    function search(page_counter,is_search){
        FormDataVal = $('#search_form').serialize();
        get_results(FormDataVal,page_counter,is_search);
    }
    var FormDataVal;
    var page_counter = 1;
    $('#search_form').on('submit',function(event){
        event.preventDefault();
        page_counter = 1;
        search(page_counter,true);
    })
    $('#load_more').on('click',function(){
        page_counter = page_counter + 1
        if(FormDataVal){
            search(page_counter,false);
        }else{
            get_results('',page_counter);
        }
    });
    get_results('',1);
    $('#cancel_add_client').on('click',function(){
        $('#add_new_client_row').fadeOut('fast');
        $('#client_container').fadeIn('slow');
    });
    $('#add_new_client_btn').on('click',function(){
        $('#add_new_client_row').fadeIn();
        $('#client_container').fadeOut();
        
    });
    
});
