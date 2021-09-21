$(document).ready(function(){
    $('#loading_ico_add').fadeOut('fast');
    function create_err_msg(message){
        msg = '<div class="alert alert-danger alert-dismissible fade show pr-4" role="alert">\
        ' +  message + '.\
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
          <span aria-hidden="true">&times;</span>\
        </button>\
      </div>'
      return msg
    }
    function create_client(dataSend){
        var response = $.ajax({
            dataType: 'json',
            method: 'POST',
            cache: false,
            url: create_assistant_url,
            data : dataSend,
            beforeSend: function () {
                $('#loading_ico_add').fadeIn('fast');
                $('#form-errors').html('')
            },
            success: function (response, status, xhr) {
                const jsonResponse = JSON.parse(response)
                assistant_id  = jsonResponse[0]['fields']['id']
                assistant_name  = jsonResponse[0]['fields']['first_name']
                assistant_email = jsonResponse[0]['fields']['email']
                console.log(assistant_id);
                // $('#add_new_client_row').fadeOut('fast');
                // $('#success_assistand_added').fadeIn('fast');
                // $('#assistant_email').html(assistant_email);
                // $('#assistant_name').html(assistant_name);
            },
            error: function (xhrObj, status, errType) {
                full_response = JSON.parse(response.responseJSON)
                fields = Object.keys(full_response)
                for (field of fields) {
                    messages = full_response[field]
                    for (let index = 0; index < messages.length; index++) {
                        const message = messages[index];
                        $('#form-errors').append(create_err_msg(message.message));
                    }
                }
                $('#form-errors').slideDown();
            },
            complete: function (xhrObj, status) {
                $('#loading_ico_add').fadeOut('fast');
            }
        });
    }
    $('#create_assistant_form').on('submit',function(){
        event.preventDefault();
        FormDataVal = $(this).serialize();
        create_client(FormDataVal);
    });
    
});
