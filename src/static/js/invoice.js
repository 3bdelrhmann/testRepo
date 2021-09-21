function get_results(query,page_num,replace,is_search){
    var response = $.ajax({
        dataType: 'json',
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        method: 'GET',
        cache: false,
        url: search_url,
        data : {
            'query' :query ,
            'page_num' : page_num,
        },
        beforeSend: function () {
            $('#loading_ico').fadeIn('fast');
            if(replace == true){
                if(is_search == true){
                    $('#invoice-title').fadeOut('fast',function(){
                        $('#invoice-title').text('نتائج البحث');
                        $('#invoice-title').fadeIn('fast')
                    });
                }
                $('#invoices_box').html('');
            }

        },
        success: function (response, status, xhr) {
            console.log(response)
            for (let index = 0; index < response.length; index++) {
                get_empty = $('#invoice_empty_box').html();
                invoice = $(get_empty).appendTo('#invoices_box').fadeIn('slow');
                const obj_id        = response[index]['id']
                const invoice_id    = response[index]['id'];
                const customer_name = response[index]['customer_name'];
                const lawyer_name   = response[index]['lawyer_name'];
                const created_at    = response[index]['created_at'];
                
                /* DELETE ATTRS*/
                $(invoice).attr('data-obj-id',obj_id);
                $(invoice).find('#delete-object').attr('data-id-delete',obj_id);
                /* DELETE ATTRS*/

                $(invoice).find('#invoice_href').attr('href','detail/'+invoice_id);
                $(invoice).find('#invoice_id').html(invoice_id);
                $(invoice).find('#customer_name').html(customer_name);
                $(invoice).find('#lawyer_name').html(lawyer_name);
                $(invoice).find('#invoice_date').html(created_at);


            }
            if(response.length == 0){
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
$(document).ready(function(){
    var page_counter = 1;
    $('#search-box').on('keyup',function(){
        page_counter = 1;
        const query  = this.value;
            get_results(query,1,true,true);
    });
    $('#load_more').on('click',function(){
        page_counter = page_counter + 1
        if($('#search-box').val()){
            get_results($('#search-box').val(),page_counter,false);
        }else{
            get_results('',page_counter,false);
        }
    });
    get_results('',1,true);
});