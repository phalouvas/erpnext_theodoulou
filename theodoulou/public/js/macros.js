function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function active_vehicle() {
    // get input element value with id vehicle_name and save in cookies
    var vehicleActiveSelectionName = document.getElementById("vehicle_name");
    // if vehicleActiveSelectionName not empty
    if (vehicleActiveSelectionName) {
        // set cookie with vehicleActiveSelectionName
        document.cookie = "vehicleActiveSelectionName=" + vehicleActiveSelectionName.value + "; sameSite=Lax; path=/";

        // Get the query string parameters
        var params = new URLSearchParams(window.location.search);

        // For each parameter, set it as a cookie
        for (var pair of params.entries()) {
            document.cookie = pair[0] + "=" + pair[1] + "; sameSite=Lax; path=/";
        }
    }

    // Get the cookie value
    var vehicle_name = getCookie('vehicleActiveSelectionName');
    var BrandClass = getCookie('BrandClass');
    var ManNo = getCookie('ManNo');
    var KModNo = getCookie('KModNo');
    var needyear = getCookie('needyear');
    var KTypNo = getCookie('KTypNo');

    // Get the span element
    // Add missing import for jQuery
    var element = $('#vehicleActiveSelectionNameTitle');

    // Set the inner HTML of the span element to the cookie value
    if (element && vehicle_name) {
        element.html(vehicle_name);
        element.attr('href', `/brands/models/types/vehicle?BrandClass=${BrandClass}&ManNo=${ManNo}&KModNo=${KModNo}&needyear=${needyear}&KTypNo=${KTypNo}`);
    }

    if (element.html() != '') {
        $('#vehicleActiveSelectionContainer').show();
    }

    $('#vehicleActiveSelectionClear').on('click', function () {
        document.cookie = 'vehicleActiveSelectionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/brands';
    });
}

$(document).ready(function () {
    active_vehicle();
});
