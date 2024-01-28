$(document).ready(function () {
    // Get the query string parameters
    var params = new URLSearchParams(window.location.search);

    // For each parameter, set it as a cookie
    for (var pair of params.entries()) {
        document.cookie = pair[0] + "=" + pair[1] + "; sameSite=Lax; path=/";
    }

    // get input element value with id vehicle_name and save in cookies
    var vehicleActiveSelectionName = document.getElementById("vehicle_name").value;
    document.cookie = "vehicleActiveSelectionName=" + vehicleActiveSelectionName + "; sameSite=Lax; path=/";
    
});