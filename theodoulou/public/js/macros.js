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
    var brand_id = getCookie('brand_id');
    var model_id = getCookie('model_id');
    var vehicle_id = getCookie('vehicle_id');
    var needyear = getCookie('needyear');

    // Get the span element
    // Add missing import for jQuery
    var element = $('#vehicleActiveSelectionNameTitle');

    // Set the inner HTML of the span element to the cookie value
    if (element && vehicle_name) {
        element.html(vehicle_name);
        element.attr('href', `/pc/models/types/vehicle?vehicle_id=${vehicle_id}&brand_id=${brand_id}&model_id=${model_id}&needyear=${needyear}`);
    }

    if (element.html() != '') {
        $('#vehicleActiveSelectionContainer').show();
    }

    $('#vehicleActiveSelectionClear').on('click', function () {
        document.cookie = 'vehicleActiveSelectionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/pc';
    });
}

function active_node() {
    // get input element value with id node_name and save in cookies
    var node_name = document.getElementById("node_name");
    var node_id = document.getElementById("node_id");
    // if node_name not empty
    if (node_name) {
        // set cookie with node_name
        document.cookie = "node_name=" + node_name.value + "; sameSite=Lax; path=/";
        document.cookie = "node_id=" + node_id.value + "; sameSite=Lax; path=/";
    }

    // Get the cookie value
    var node_name = getCookie('node_name');
    var node_id = getCookie('node_id');
}

$(document).ready(function () {
    active_node();
    active_vehicle();
});
