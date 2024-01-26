$(document).ready(function () {
    // Get all the collapsible headers
    var coll = document.getElementsByClassName("collapsible-header");

    // Add a click event listener to each header
    for (var i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            // Toggle the visibility of the body
            var body = this.nextElementSibling;
            body.style.display = body.style.display === "none" ? "block" : "none";
        });
    }
});