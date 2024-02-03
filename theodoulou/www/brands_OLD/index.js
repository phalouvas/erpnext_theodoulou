$(document).ready(function() {
    $('#passenger_cars_searchKey').on('keyup', function() {
        var searchKey = $(this).val().toLowerCase();

        $('.passenger_cars_card_container').each(function() {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('#commercial_cars_searchKey').on('keyup', function() {
        var searchKey = $(this).val().toLowerCase();

        $('.commercial_cars_card_container').each(function() {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Check if the vehicle_type cookie is set
    var vehicle_type = document.cookie.split('; ').find(row => row.startsWith('vehicle_type='));

    // If the vehicle_type cookie is not set, set it to "PKW"
    if (!vehicle_type) {
        document.cookie = "vehicle_type=PKW";
        vehicle_type = "vehicle_type=PKW";
    }

    if (vehicle_type == "vehicle_type=PKW") {
        $('#brandsTab li:first-child a').tab('show')
    } else {
        $('#brandsTab li:last-child a').tab('show')
    }

    // If the element with ID passenger_cars-tab is clicked, set the cookie to "PKW"
    $('#passenger_cars-tab').click(function() {
        document.cookie = "vehicle_type=PKW";
    });

    // If the element with ID commercial_cars-tab is clicked, set the cookie to "NKW"
    $('#commercial_cars-tab').click(function() {
        document.cookie = "vehicle_type=NKW";
    });

});