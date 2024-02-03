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

        $('.clearSearch').on('click', function () {
            $('#searchKey').val('');
            $('.searchContainer').show();
        });
    });
});