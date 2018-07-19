$(function() {
    // Toolbar Handlers
    var htkToolbarHandle = $('.htk-toolbar-handle');
    var htkToolbar = $('.htk-toolbar');
    var htkToolbarHideButton = $('.htk-toolbar-hide');
    var HTK_EMULATE_USER_COOKIE_EXPIRE_TIME_SECONDS = 15 * 60 * 1000 // 15 minutes

    // User ID elements
    var emulateUserIDContainer = $('.emulate-user-id');
    var emulateUserIDButton = $('.emulate-form-user-id .emulate-button');
    var emulateUserIDStopButton = $('.emulate-user-id-stop');
    var EMULATE_USER_ID = 'emulate_user_id';

    // Username elements
    var emulateUsernameContainer = $('.emulate-username');
    var emulateUsernameButton = $('.emulate-form-username .emulate-button');
    var emulateUsernameStopButton = $('.emulate-username-stop');
    var EMULATE_USERNAME = 'emulate_user_username';

    function setPulsatingHtkToolBarHandle() {
        if ($.cookie(EMULATE_USER_ID) || $.cookie(EMULATE_USERNAME)) {
            htkToolbarHandle.addClass('pulsating-htk-toolbar-handle');
        } else {
            htkToolbarHandle.removeClass('pulsating-htk-toolbar-handle');
        }
    }

    function toggleContainers() {
        if ($.cookie(EMULATE_USER_ID)) {
            emulateUsernameContainer.hide();
        } else if ($.cookie(EMULATE_USERNAME)) {
            emulateUserIDContainer.hide();
        } else {
            emulateUserIDContainer.show();
            emulateUsernameContainer.show();
        }
    }

    function toggleForm(formName) {
        var form = $('.emulate-form-' + formName);
        var stopButton = $('.emulate-' + formName + '-stop');
        var cookieName = getCookieName(formName);
        if ($.cookie(cookieName)) {
            form.hide();
            stopButton.show();
        } else  {
            form.show();
            stopButton.hide();
        }
    }

    function get_expire_date() {
        var date = new Date();
        date.setTime(date.getTime() + HTK_EMULATE_USER_COOKIE_EXPIRE_TIME_SECONDS);
        return date;
    }

    function getCookieName(name) {
        var cookieNameSplit = name.split('-');
        var cookieName = 'emulate_user_' + cookieNameSplit[cookieNameSplit.length - 1];
        return cookieName;
    }

    function emulateButtonClicked(buttonName) {
        var input = $('.emulate-form-' + buttonName + ' .emulate-input');
        var cookieName = getCookieName(buttonName);
        var cookieVal = input.val();
        $.cookie(cookieName, cookieVal, { expires: get_expire_date() });
        location.reload();
    }

    function removeCookie(cookieName) {
        $.removeCookie(cookieName, null);
        location.reload();
    }

    function toggleToolbar() {
        if (htkToolbar.is(':visible')) {
            htkToolbar.hide();
            htkToolbarHandle.show();
        } else {
            htkToolbar.show();
            htkToolbarHandle.hide();
        }
    }

    function initEventHandlers() {
        htkToolbarHandle.click(toggleToolbar);
        htkToolbarHideButton.click(toggleToolbar);
        emulateUserIDButton.click(emulateButtonClicked.bind(null, 'user-id'));
        emulateUsernameButton.click(emulateButtonClicked.bind(null, 'username'));
        emulateUserIDStopButton.click(removeCookie.bind(null, EMULATE_USER_ID));
        emulateUsernameStopButton.click(removeCookie.bind(null, EMULATE_USERNAME));
    }

    function init() {
        toggleContainers();
        toggleForm('user-id');
        toggleForm('username');
        setPulsatingHtkToolBarHandle();
    }

    initEventHandlers();
    init();
});
