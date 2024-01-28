$(document).ready(function () {
    $('.tree .caret').on('click', function () {
        $(this).toggleClass('caret-down');
        $(this).siblings('ul').toggle();
    });
});