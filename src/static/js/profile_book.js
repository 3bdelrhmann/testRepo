$(document).ready(function() {
    function create_err_msg(message){
        msg = '<div class="alert alert-danger alert-dismissible fade show pr-4" role="alert">\
        ' +  message + '.\
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
          <span aria-hidden="true">&times;</span>\
        </button>\
      </div>'
      return msg
    }
    $('#phSession_form').on('submit',function(){
        event.preventDefault();
        const FormData = $(this).serialize();
        var response = $.ajax({
            dataType: 'json',
            method: 'POST',
            cache: false,
            url: phSession_book_url,
            data : FormData,
            beforeSend: function () {
                $('#form_errors').html('')
            },
            success: function (response, status, xhr) {
                if(xhr.status == 201){
                    $('#form_inputs').fadeOut('fast');
                    $('#book_success').fadeIn("fast");
                }
                console.log(response)
            },
            error: function (response, status, errType) {
                full_response = JSON.parse(response.responseJSON)
                fields = Object.keys(full_response)
                for (field of fields) {
                    messages = full_response[field]
                    for (let index = 0; index < messages.length; index++) {
                        const message = messages[index];
                        $('#form_errors').append(create_err_msg(message.message));
                    }
                }
            },
            compelete: function (response, status) {
            }
        });
    
    })

})