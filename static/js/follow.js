YUI().use(
    'node',
    'event',
    'cookie',
    'io',
    'json',
function (Y) {
    // --------------------------------------------------
    // YUI "Local" Globals

    // CSS selectors
    var CSS_CLASS_FOLLOW_BUTTON = 'follow-button';
    var CSS_CLASS_FOLLOWING = 'following';
    var CSS_CLASS_NOT_FOLLOWING = 'not-following';
    var CSS_CLASS_FOLLOW = 'follow';
    var CSS_CLASS_UNFOLLOW = 'unfollow';

    // Nodes
    var main = Y.one('#main');

    // App variables
    var IO_TRANSACTION_DATA = {};

    // Custom attributes
    var ATTR_DATA_FOLLOW_URI = 'data:follow-uri';
    var ATTR_DATA_UNFOLLOW_URI = 'data:unfollow-uri';

    var S_FOLLOW_API_ERROR = 'Bad JSON response received from Follow API Call';

    // End YUI "Local" Globals
    // --------------------------------------------------

    // Custom App Functions

    function handleFollowUnfollowButtonPressed(e) {
        var button = this;
        var isFollowing = button.hasClass(CSS_CLASS_FOLLOWING);
        var follow = button.one('.' + CSS_CLASS_FOLLOW);
        var unfollow = button.one('.' + CSS_CLASS_UNFOLLOW);
        var uri;

        if (isFollowing) {
            uri = unfollow.getAttribute(ATTR_DATA_UNFOLLOW_URI);
        } else {
            uri = follow.getAttribute(ATTR_DATA_FOLLOW_URI);
        }

        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            on: {
                complete: handleFollowUnfollowComplete
            }
        };

        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            button: button,
            isFollowing: isFollowing
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    // --------------------------------------------------
    // IO Callbacks
    function handleFollowUnfollowComplete(transactionId, response, args) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push(S_FOLLOW_API_ERROR);
        }

        if (responseData) {
            var status = responseData['status'];
            if (status === 'okay') {
                var transactionData = IO_TRANSACTION_DATA[transactionId];
                var button = transactionData.button;
                var isFollowing = transactionData.isFollowing;
                if (isFollowing) {
                    button.replaceClass(CSS_CLASS_FOLLOWING, CSS_CLASS_NOT_FOLLOWING);
                } else {
                    button.replaceClass(CSS_CLASS_NOT_FOLLOWING, CSS_CLASS_FOLLOWING);
                }
            }
        }
    }

    // App Initializers
    function initEventHandlers() {
        main.delegate('click', handleFollowUnfollowButtonPressed, '.' + CSS_CLASS_FOLLOW_BUTTON);
    }

    function init() {
    }
    initEventHandlers();
    init();
});
