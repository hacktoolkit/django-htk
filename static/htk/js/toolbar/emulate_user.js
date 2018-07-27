$(function() {
    // Toolbar Elements
    var htkToolbar = $('.htk-toolbar');
    var htkToolbarHideButton = $('.htk-toolbar-hide');
    var htkToolbarTab = $('.htk-toolbar-tab');

    // Toolbar Constants
    var EMULATE_USER_ID = 'emulate_user_id';
    var EMULATE_USERNAME = 'emulate_user_username';
    var HTK_EMULATE_USER_COOKIE_EXPIRE_TIME_SECONDS = HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES * 60 * 1000;

    // Elements
    var emulateUserForm = $('.emulate-user-form');
    var emulateUserIDButton = $('.emulate-user-form button.user-id');
    var emulateUsernameButton = $('.emulate-user-form button.username');
    var emulateUserStopButton = $('.emulate-user-stop');
    var emulateUserInput = $('.emulate-user-form input');
    var emulateUserMessage = $('.emulate-user-message');

    function getActiveCookie() {
        return $.cookie(EMULATE_USER_ID) || $.cookie(EMULATE_USERNAME);
    }

    function getExpireDate() {
        var date = new Date();
        date.setTime(date.getTime() + HTK_EMULATE_USER_COOKIE_EXPIRE_TIME_SECONDS);
        return date;
    }

    function setPulsatingHtkToolBarHandle() {
        if ($.cookie(EMULATE_USER_ID) || $.cookie(EMULATE_USERNAME)) {
            htkToolbarTab.addClass('pulsating-htk-toolbar-tab');
        } else {
            htkToolbarTab.removeClass('pulsating-htk-toolbar-tab');
        }
    }

    function toggleForm() {
        var activeCookie = getActiveCookie();
        if (activeCookie) {
            emulateUserForm.hide();
            emulateUserStopButton.show();
        } else  {
            emulateUserForm.show();
            emulateUserStopButton.hide();
        }
    }

    function showError() {
        emulateUserMessage.html('Invalid Username or User ID');
        emulateUserMessage.show();
    }

    function handleEmulateUserButtonClicked(cookieName) {
        var cookieVal = emulateUserInput.val();
        if (cookieVal === '' || (cookieName === EMULATE_USER_ID && isNaN(cookieVal))) {
            showError();
            return;
        }

        emulateUserMessage.hide();
        $.cookie(cookieName, cookieVal, { expires: getExpireDate() });
        location.reload();
    }

    function handleEmulateUserStopButtonClicked() {
        var cookieName;
        if ($.cookie(EMULATE_USER_ID)) {
            cookieName = EMULATE_USER_ID;
        } else if ($.cookie(EMULATE_USERNAME)) {
            cookieName = EMULATE_USERNAME;
        }
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
        emulateUserIDButton.click(handleEmulateUserButtonClicked.bind(null, EMULATE_USER_ID));
        emulateUsernameButton.click(handleEmulateUserButtonClicked.bind(null, EMULATE_USERNAME));
        emulateUserStopButton.click(handleEmulateUserStopButtonClicked);
        htkToolbarTab.click(handleToggleToolbar);
        htkToolbarHideButton.click(handleToggleToolbar);
    }

    function init() {
        toggleForm();
        setPulsatingHtkToolBarHandle();
    }

    initEventHandlers();
    init();
});
