function start_counter(seconds){
    $('#counter').addClass('blink');
    $('.resend-btn').removeClass('btn-base');
    $('#resend-btn').prop('disabled',true);
    $('.resend-btn').addClass('custom-disabled');
    var timeleft = seconds;
    var downloadTimer = setInterval(function(){
      if(timeleft <= 0){
        clearInterval(downloadTimer);
        document.getElementById("counter").innerHTML = 0;
        $('#counter').removeClass('blink');
        $('.resend-btn').removeClass('blink custom-disabled');
        $('.resend-btn').addClass('btn-base');
        $('.resend-btn').removeAttr('disabled');
        $('#resend-btn').on('click',function(){
          location.reload(true);
        })
      } else{
        document.getElementById("counter").innerHTML = timeleft;
      }
      timeleft -= 1;
    }, 1000);

}
function resend_req(){
  $.ajax({
    dataType: 'json',
    headers: { "X-CSRFToken": getCookie('csrftoken') },
    method: 'GET',
    cache: false,
    url: resend_url,
    beforeSend: function () {
    },
    success: function (response, status, xhr) {
        let data = JSON.parse(response);
        start_counter(parseInt(data['reminder']));
    },
    error: function (xhrObj, status, errType) {
    },
    complete: function (xhrObj, status) {
    }
})

}
$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');
    resend_req();
    $('#resend-btn').on('click',function(){
      resend_req();
    });
    

});