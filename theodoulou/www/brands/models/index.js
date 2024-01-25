$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    var needYear = urlParams.get('NEEDYEAR');
    var searchKey = urlParams.get('SEARCHKEY');

    if (needYear) {
        $('#models_yearFilter').val(needYear);
    }

    if (searchKey) {
        $('#models_searchKey').val(searchKey);

        $('.models_card_container').each(function() {
            var name = $(this).data('name');
            // if name is numeric convert to string
            name = name + '';

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $('#models_searchKey').on('keyup', function() {
        searchKey = $(this).val().toLowerCase();

        $('.models_card_container').each(function() {
            var name = $(this).data('name');
            // if name is numeric convert to string
            name = name + '';

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('#models_yearFilter').on('change', function() {
        var selectedYear = $(this).val();
        var url = new URL(window.location.href);
        url.searchParams.set('NEEDYEAR', selectedYear);
        url.searchParams.set('SEARCHKEY', $('#models_searchKey').val());
        window.location.href = url.toString();
    });
});