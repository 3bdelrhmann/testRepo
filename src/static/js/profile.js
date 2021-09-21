$(document).ready(function(){
    function get_results(lawyer_id,page_num){
        var response = $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'GET',
            cache: false,
            url: lwReviews,
            data : {
                'lawyer_id' :lawyer_id ,
                'page_num' : page_num,
            },
            beforeSend: function () {
                $('#loading_ico').fadeIn('fast');
            },
            success: function (response, status, xhr) {
                for (let index = 0; index < response.length; index++) {
                    created_at  = new Date(response[index]['created_at'])
                    comment = response[index]['comment']
                    rate    = response[index]['rate']
                    $('#empty_review #comment').html(comment);
                    $('#empty_review #rate').attr({'data-rating-value':rate});
                    $('#empty_review #customer_info').html(created_at.getFullYear()+'-'+created_at.getMonth()+'-'+created_at.getDate());
                    reveiw = $('#empty_review').html();
                    $(reveiw).appendTo('#all_reviews').fadeIn('fast');
                }
                if(response.length == 0){
                    $('#load_more').removeClass('btn-base');
                    $('#load_more').addClass('custom-disabled');
                    $('#load_more').attr('disabled',true);
                }
            },
            error: function (xhrObj, status, errType) {
            },
            
            complete: function (xhrObj, status) {
                $('#loading_ico').fadeOut();
            }
        });
    }
    var lawyer_id    = $('[name=lawyer_id]').val();
    var page_counter = 1;
    // var standard_hight = 120;
    $('#load_more').on('click',function(){
        // standard_hight = standard_hight + 120
        // $('#all_reviews').animate({height: standard_hight });
        page_counter = page_counter + 1
        get_results(lawyer_id,page_counter);
    });
    get_results(lawyer_id,page_counter);

});
