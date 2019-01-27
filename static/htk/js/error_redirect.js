$(function() {
    /* -------------------------------------------------- */
    /* "Local" Globals */

    // CSS selectors

    // Nodes
    var main = $('#main');

    // App variables

    /* End "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions
    function redirectHome() {
        // TODO: animate countdown
        setTimeout(
            function() {
                document.location = '/';
            },
            5000
        );
    }

    // App Initializers
    function initEventHandlers() {
    }

    function init() {
        redirectHome();
    }
    initEventHandlers();
    init();
});
