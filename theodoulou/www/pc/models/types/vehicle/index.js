$(document).ready(function () {
    // Get the query string parameters
    var params = new URLSearchParams(window.location.search);

    // For each parameter, set it as a cookie
    for (var pair of params.entries()) {
        document.cookie = pair[0] + "=" + pair[1];
    }

    // get element data-name attribute value with id vehicle-active-selection-name and save in cookies
    var vehicleActiveSelectionName = document.getElementById("vehicleActiveSelectionName").getAttribute("data-name");
    document.cookie = "vehicleActiveSelectionName=" + vehicleActiveSelectionName + "; sameSite=Lax; path=/";

    $('#vehicleActiveSelectionClear').on('click', function () {
        document.cookie = 'vehicleActiveSelectionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/pc';
    });

    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });
});