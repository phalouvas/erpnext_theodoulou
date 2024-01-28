$(document).ready(function () {

    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });

    // Get the cookie value
    var name = 'vehicleActiveSelectionName=';
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            var cookieValue = c.substring(name.length, c.length);
        }
    }

    // Get the span element
    var element = document.getElementById('vehicleActiveSelectionNameTitle');

    // Set the inner HTML of the span element to the cookie value
    if (element && cookieValue) {
        element.innerHTML = cookieValue;
    }

    if (element.innerHTML == '') {
        $('#vehicleActiveSelectionContainer').hide();
    }

    $('#vehicleActiveSelectionClear').on('click', function () {
        document.cookie = 'vehicleActiveSelectionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/pc';
    });
});
