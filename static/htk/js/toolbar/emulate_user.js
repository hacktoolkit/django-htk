$(function() {
    // Toolbar Elements
    var htkToolbar = $('.htk-toolbar');
    var htkToolbarHideButton = $('.htk-toolbar-hide');
    var htkToolbarTab = $('.htk-toolbar-tab');

    // Toolbar Constants
    var EMULATE_USER_ID = 'emulate_user_id';
    var EMULATE_USERNAME = 'emulate_user_username';
    var HTK_EMULATE_USER_COOKIE_EXPIRE_TIME_SECONDS = HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES * 60 * 1000;

    // User ID elements
    var emulateUserIDButton = $('.emulate-user-id-form .emulate-button');
    var emulateUserIDContainer = $('.emulate-user-id');
    var emulateUserIDStopButton = $('.emulate-user-id-stop');

    // Username elements
    var emulateUsernameContainer = $('.emulate-username');
    var emulateUsernameButton = $('.emulate-username-form .emulate-button');
    var emulateUsernameStopButton = $('.emulate-username-stop');

    function setPulsatingHtkToolBarHandle() {
        if ($.cookie(EMULATE_USER_ID) || $.cookie(EMULATE_USERNAME)) {
            htkToolbarTab.addClass('pulsating-htk-toolbar-tab');
        } else {
            htkToolbarTab.removeClass('pulsating-htk-toolbar-tab');
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
        var form = $('.emulate-' + formName + '-form');
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
        var cookieNameParts = name.split('-');
        var cookieName = 'emulate_user_' + cookieNameParts[cookieNameParts.length - 1];
        return cookieName;
    }

    function handleEmulateUserButtonClicked(buttonName) {
        var input = $('.emulate-' + buttonName + '-form .emulate-input');
        var cookieName = getCookieName(buttonName);
        var cookieVal = input.val();
        $.cookie(cookieName, cookieVal, { expires: get_expire_date() });
        location.reload();
    }

    function handleEmulateUserStopButtonClicked(cookieName) {
        $.removeCookie(cookieName, null);
        location.reload();
    }

    function handleToggleToolbar() {
        if (htkToolbar.is(':visible')) {
            htkToolbar.hide();
            htkToolbarTab.show();
        } else {
            htkToolbar.show();
            htkToolbarTab.hide();
        }
    }

    function initEventHandlers() {
        emulateUserIDButton.click(handleEmulateUserButtonClicked.bind(null, 'user-id'));
        emulateUserIDStopButton.click(handleEmulateUserStopButtonClicked.bind(null, EMULATE_USER_ID));
        emulateUsernameButton.click(handleEmulateUserButtonClicked.bind(null, 'username'));
        emulateUsernameStopButton.click(handleEmulateUserStopButtonClicked.bind(null, EMULATE_USERNAME));
        htkToolbarTab.click(handleToggleToolbar);
        htkToolbarHideButton.click(handleToggleToolbar);
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
