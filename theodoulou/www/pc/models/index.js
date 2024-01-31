$(document).ready(function() {

    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });
    
    var urlParams = new URLSearchParams(window.location.search);
    var needYear = urlParams.get('needyear');
    var searchKey = urlParams.get('searchkey');

    if (needYear) {
        $('#yearFilter').val(needYear);
    }

    if (searchKey) {
        $('#searchKey').val(searchKey);

        $('.searchContainer').each(function() {
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

    $('#searchKey').on('keyup', function() {
        searchKey = $(this).val().toLowerCase();

        $('.searchContainer').each(function() {
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

    $('#yearFilter').on('change', function() {
        var selectedYear = $(this).val();
        var url = new URL(window.location.href);
        url.searchParams.set('needyear', selectedYear);
        url.searchParams.set('searchkey', $('#searchKey').val());
        window.location.href = url.toString();
    });

    $('.clearSearch').on('click', function() {
        $('#searchKey').val('');
        $('#yearFilter').val('0');
        var url = new URL(window.location.href);
        url.searchParams.delete('searchkey');
        url.searchParams.set('needyear', $('#yearFilter').val());
        window.location.href = url.toString();
    });
});