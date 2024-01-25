$(document).ready(function() {
    $('#models_searchKey').on('keyup', function() {
        var searchKey = $(this).val().toLowerCase();

        $('.models_card_container').each(function() {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});