$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    var needYear = urlParams.get('needyear');
    var searchKey = urlParams.get('searchkey');

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
        url.searchParams.set('needyear', selectedYear);
        url.searchParams.set('searchkey', $('#models_searchKey').val());
        window.location.href = url.toString();
    });

    $('#resetFilter').on('click', function() {
        $('#models_searchKey').val('');
        $('#models_yearFilter').val('0');
        var url = new URL(window.location.href);
        url.searchParams.delete('searchkey');
        url.searchParams.set('needyear', $('#models_yearFilter').val());
        window.location.href = url.toString();
    });
});