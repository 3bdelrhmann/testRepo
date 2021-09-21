$(document).ready(function(){
    $('#office_address').on('change click keyup',function(){
        let country = $('#country').val();
        let region  = $('#regions').val();
        let governorate    = $('#governorate').val();
        let office_address = this.value;
        country = document.querySelector('#country option[value="'+country+'"]').textContent
        region  = document.querySelector('#regions option[value="'+region+'"]').textContent
        governorate  = document.querySelector('#governorate option[value="'+governorate+'"]').textContent
        $('#address_sample').html(office_address + ',' + region + ','+ governorate + ',' + country);
    });

    $('#governorate').on('click',function(){
        const country = $('#country').val();
        console.log(country);
        $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'GET',
            cache: false,
            url: gov_url,
            data : {
                'country' : country,
            },
            beforeSend: function () {
            },
            success: function (response, status, xhr) {
                let all_govs = '';
                for (let index = 0; index < response.length; index++) {
                    let gov_id   = response[index].id
                    let gov_name = response[index].name
                    all_govs += '<option value="'+ gov_id +'">'+ gov_name +'</option>';
                }
                $('#governorate').html(all_govs);

            },
            error: function (xhrObj, status, errType) {
            },
            complete: function (xhrObj, status) {
            }
        });
    });
    $('#regions').on('click',function(){
        const governorate = $('#governorate').val();
        $.ajax({
            dataType: 'json',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            method: 'GET',
            cache: false,
            url: regions_url,
            data : {
                'governorate' : governorate,
            },
            beforeSend: function () {
            },
            success: function (response, status, xhr) {
                let all_regions = '';
                for (let index = 0; index < response.length; index++) {
                    let region_id   = response[index].id
                    let region_name = response[index].name
                    all_regions += '<option value="'+ region_id +'">'+ region_name +'</option>';
                }
                $('#regions').html(all_regions);
            },
            error: function (xhrObj, status, errType) {
            },
            complete: function (xhrObj, status) {
            }
        });
    });

});