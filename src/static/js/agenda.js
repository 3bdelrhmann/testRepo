$(document).ready(function(){

    function get_results(form_data,page_num,is_search=false,session_date){
        if(form_data){
            form_data = form_data + '&page_num=' +  page_num;
            dataSend  = form_data
            if(session_date){
                add_date = dataSend + '&session_date=' +  session_date;
                dataSend = add_date
            }
        }else{
            dataSend = {
                'page_num' : page_num,
                // 'date'  : today,
            }
            if(session_date){
                dataSend['session_date'] = session_date

            }
        }
        var response = $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'GET',
            cache: false,
            url: agenda_search_url,
            data : dataSend,
            beforeSend: function () {
                $('#loading_ico').fadeIn('fast');
                if(is_search == true){
                    SpecficDate  = null;
                        $('#agenda-title').fadeOut('fast',function(){
                        $('#agenda-title').text('نتائج البحث');
                        $('#agenda-title').fadeIn('fast')
                    });
                    $('#agenda_box').html('');
                }
            },
            success: function (response, status, xhr) {
                for (let index = 0; index < response.length; index++) {
                    get_empty = $('#agenda_empty').html();
                    reveiw = $(get_empty).appendTo('#agenda_box').fadeIn('slow');
                    
                    obj_id    = response[index]['id']
                    case_id   = response[index]['case_id']
                    case_year = response[index]['case_year']
                    notes     = response[index]['notes']
                    court     = response[index]['court']
                    session_date    = response[index]['session_date']
                    customer_name   = response[index]['customer_name']
                    customer_mobile = response[index]['customer_mobile']

                    // alert(update_url);
                    $(reveiw).find('#agenda_update_url').attr('href',update_agenda_url+obj_id);

                    $(reveiw).attr('data-obj-id',obj_id);
                    $(reveiw).find('#delete-object').attr('data-id-delete',obj_id);
                    $(reveiw).find('#customer_name').html(customer_name);
                    $(reveiw).find('#customer_name').html(customer_name);
                    $(reveiw).find('#mobile_number_href').attr('href','tel:'+customer_mobile);
                    $(reveiw).find('#customer_mobile').html(customer_mobile);
                    $(reveiw).find('#copy_mobile').html(customer_mobile);
                    $(reveiw).find('#copy_mobile').html(customer_mobile);
                    $(reveiw).find('#session_date').html(session_date);
                    $(reveiw).find('#court').html(court);
                    $(reveiw).find('#case_year').html(case_year);
                    $(reveiw).find('#case_id').html(case_id);
                    $(reveiw).find('#notes').html(notes);
                }
                if(response.length == 0){
                    if(is_search == true){
                        $('#agenda_box').html('');
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
    var SpecficDate  = null;
    var page_counter = 1;

    $('.get_date_results').on('click',function(){
        const session_date = $(this).attr('data-date');
        get_results('',1,true,session_date);
        SpecficDate = session_date
    })
    $('#search_form').on('submit',function(){
        page_counter = 1;
        search(page_counter,true);
    })
    $('#load_more').on('click',function(){
        page_counter = page_counter + 1
        if(FormDataVal){
            search(page_counter,false);
        }else{
            if(SpecficDate){
                get_results('',page_counter,false,SpecficDate);
            }else{
                get_results('',page_counter);
            }
        }
    });
    get_results('',1);
    $('#search_date').datepicker({
        maxViewMode: 2,
        startView: 1,
        language: "ar",
        autoclose: true,
        todayHighlight: true,
        format: 'yyyy-mm-dd',
        orientation: "bottom auto",
    });
});
