$(document).ready(function () {
    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });

    $('#searchKey_OE').on('keyup', function () {
        var searchKey = $(this).val().toLowerCase();

        $('.searchContainer_OE').each(function () {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('#searchKey_VEH').on('keyup', function () {
        var searchKey = $(this).val().toLowerCase();

        $('.searchContainer_VEH').each(function () {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});