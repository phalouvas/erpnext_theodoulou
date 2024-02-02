$(document).ready(function () {
    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });

    $('#searchKey').on('keyup', function () {
        var searchKey = $(this).val().toLowerCase();

        $('.searchContainer').each(function () {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('.clearSearch').on('click', function () {
        $('#searchKey').val('');
        $('.searchContainer').show();
    });

    $('.showAll').on('click', function () {
        var url = window.location.href;
        var separator = (url.indexOf('?') !== -1) ? "&" : "?";
        window.location.href = url + separator + 'show_all=1';
    });

    $('.showPopular').on('click', function () {
        // remove the show_all parameter
        var url = window.location.href;
        url = url.replace(/&?show_all=1/, '');
        window.location.href = url;
    });

    var params = new URLSearchParams(window.location.search);
    if (params.has('show_all')) {
        $('.showAll').hide();
        $('.showPopular').show();
    } else {
        $('.showAll').show();
        $('.showPopular').hide();
    }
});