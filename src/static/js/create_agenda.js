$(document).ready(function(){
    $('#session_date').datepicker({
        maxViewMode: 2,
        startView: 2,
        language: "ar",
        autoclose: true,
        format: 'yyyy-mm-dd',
        orientation: "bottom auto",
        startDate: '1950-12-31',
        });
})