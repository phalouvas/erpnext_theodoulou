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

    $('#toggleButton').on('click', function() {
        $('#passenger_cars, #commercial_cars').toggle();

        if ($(this).text() === 'Click to show Commercial Cars') {
            $(this).text('Click to show Passenger Cars');
        } else {
            $(this).text('Click to show Commercial Cars');
        }
    });
});