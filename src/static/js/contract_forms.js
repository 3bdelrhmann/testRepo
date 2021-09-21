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
            url: contracts_search_url,
            data : dataSend,
            beforeSend: function() {
                if(is_search == true){
                    $('#contract_box').html('');
                }
                $('#loading_ico').fadeIn('fast');
            },
            success: function (response, status, xhr) {
                console.log(response)
                for (let index = 0; index < response.length; index++) {
                    contract_title  = response[index]['title']
                    contract_text   = $(response[index]['contract']).text().substring(1,240)
                    contract_url    = response[index]['contract_file']
                    $('#contract_empty #contract_title').html(contract_title);
                    $('#contract_empty #download_url').attr('href',contract_url);
                    $('#contract_empty #contract_preview').html(contract_text);
                    reveiw = $('#contract_empty').html();
                    $(reveiw).appendTo('#contract_box').fadeIn();
                }
                if(response.length == 0){
                    if(is_search == true){
                        $('#contract_box').html('');
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

    
});
