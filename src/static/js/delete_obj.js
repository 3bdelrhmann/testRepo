$(document).ready(function(){
    function delete_obj(delete_obj_id){
        dataSend = {
            'delete_obj_id' : delete_obj_id,
        }
        var response = $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'DELETE',
            cache: false,
            url: delete_obj_url,
            data : dataSend,
            beforeSend:function(){
                $('#delete-content').fadeOut('fast',function(){
                    $('.delete-loading#loading_ico').fadeIn('fast');
                });
            },
            success:function (response, status, xhr){
                $('[data-obj-id='+delete_obj_id+']').fadeOut('fast',function(){
                    $('#DeleteModalConfirmation').modal('hide');
                });
            },
            error:function (xhrObj, status, errType){
                
            },
            complete: function (xhrObj, status) {
                $('#delete-content').fadeIn('fast',function(){
                    $('.delete-loading#loading_ico').fadeOut('fast');
                });
            }
        });
    }
    $(document).on('click','#delete-object', function (){
        const id = $(this).attr('data-id-delete');
        $('#ConfirmationDeleteBtn').on('click',function(){
            delete_obj(id);

        })
    });
})