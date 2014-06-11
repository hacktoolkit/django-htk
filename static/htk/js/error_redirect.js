YUI().use(
    'node',
    'gallery-timer',
function (Y) {
    /* -------------------------------------------------- */
    /* YUI "Local" Globals */

    // CSS selectors

    // Nodes
    var main = Y.one('#main');

    // App variables

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions
    function redirectHome() {
        var cfg = {
            callback: function() {},
            repeatCount: 5,
            length: 1000
        }
        // TODO: animate countdown
        var t = new Y.Timer(cfg);
        t.on('timer:stop', function(e) { document.location='/'; } );
        t.start();
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
