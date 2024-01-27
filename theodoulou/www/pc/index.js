$(document).ready(function () {
    $(document).ready(function () {
        console.log('brands.js loaded');
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
        }
        );
    });
});