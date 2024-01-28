$(document).ready(function () {    
    // Get the query string parameters
    var params = new URLSearchParams(window.location.search);

    // For each parameter, set it as a cookie
    for (var pair of params.entries()) {
        document.cookie = pair[0] + "=" + pair[1];
    }
});