function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

$(document).ready(function () {

    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });

    // Get the cookie value
    var vehicle_name = getCookie('vehicleActiveSelectionName');
    var brand_id = getCookie('brand_id');
    var model_id = getCookie('model_id');
    var vehicle_id = getCookie('vehicle_id');
    var needyear = getCookie('needyear');

    // Get the span element
    // Add missing import for jQuery
    $(document).ready(function () {
        var element = $('#vehicleActiveSelectionNameTitle');

        // Set the inner HTML of the span element to the cookie value
        if (element && vehicle_name) {
            element.html(vehicle_name);
            element.attr('href', `/pc/models/types/vehicle?vehicle_id=${vehicle_id}&brand_id=${brand_id}&model_id=${model_id}&needyear=${needyear}`);
        }

        if (element.html() == '') {
            $('#vehicleActiveSelectionContainer').hide();
        }
    });

    $('#vehicleActiveSelectionClear').on('click', function () {
        document.cookie = 'vehicleActiveSelectionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/pc';
    });
});
