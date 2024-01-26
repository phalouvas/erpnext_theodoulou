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

    $('#brandsTab li:first-child a').tab('show')
});