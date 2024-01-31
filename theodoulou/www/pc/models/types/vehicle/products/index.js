$(document).ready(function () {
    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });

    // Listen for changes on the select element
    $('#searchType').on('change', function () {
        // Get the selected value
        var manufacturer_id = $(this).val();

        // Add it as a query parameter to the current URL
        var url = new URL(window.location.href);
        url.searchParams.set('manufacturer_id', manufacturer_id);
        url.searchParams.delete('page');

        // Reload the page
        window.location.href = url.href;
    });

    // On page load
    var url = new URL(window.location.href);
    var manufacturer_id = url.searchParams.get('manufacturer_id');
    if (manufacturer_id) {
        // Set the select element to the corresponding value
        $('#searchType').val(manufacturer_id);
    }
});