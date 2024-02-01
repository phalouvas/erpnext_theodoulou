$(document).ready(function () {
    $('#searchKey_ANA').on('keyup', function () {
        var searchKey = $(this).val().toLowerCase();

        $('.searchContainer_ANA').each(function () {
            var name = $(this).data('name');

            if (name.indexOf(searchKey) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});