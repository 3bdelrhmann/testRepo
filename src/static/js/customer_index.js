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
            url: clients_search_url,
            data : dataSend,
            beforeSend: function() {

                if(is_search == true){
                    $('#customers-title').fadeOut('fast',function(){
                        $('#customers-title').text('نتائج البحث');
                        $('#customers-title').fadeIn('fast')
                    });

                    $('#clients_box').html('');
                }
                $('#loading_ico').fadeIn('fast');
            },
            success: function (response, status, xhr) {
                for (let index = 0; index < response.length; index++) {
                    get_empty = $('#client_empty_box').html();
                    fetched_  = $(get_empty).appendTo('#clients_box').fadeIn('slow');

                    
                    customer_mobile = response[index]['customer_mobile']
                    customer_name   = response[index]['customer_name']
                    file_id         = response[index]['file_id']
                    notes           = response[index]['notes']
                    obj_id          = response[index]['id']
                    
                    $(fetched_).attr('data-obj-id',obj_id);
                    $(fetched_).find('#delete-object').attr('data-id-delete',obj_id);
                    $(fetched_).find('#update_client').attr('href',update_obj_url+obj_id);

                    $(fetched_).find('#client_file_id').html(file_id)
                    $(fetched_).find('#client_mobile_number_href').attr('href','tel:'+customer_mobile);
                    $(fetched_).find('#client_mobile_number').html(customer_mobile)
                    $(fetched_).find('#client_notes').html(notes)
                    $(fetched_).find('#client_name').html(customer_name)

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
        event.preventDefault();
        get_results(FormDataVal,page_counter,is_search);
    }
    var FormDataVal;
    var page_counter = 1;
    $('#search_form').on('submit',function(){
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
