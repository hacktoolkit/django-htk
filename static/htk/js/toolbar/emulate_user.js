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
    var emulateUserTitle = $('.emulate-user-title');
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
        var activeCookie = getActiveCookie();
        if (activeCookie) {
            htkToolbarTab.addClass('pulsating-htk-toolbar-tab');
        } else {
            htkToolbarTab.removeClass('pulsating-htk-toolbar-tab');
        }
    }

    function toggleForm() {
        var activeCookie = getActiveCookie();
        if (activeCookie) {
            emulateUserTitle.html(`Emulating User: ${activeCookie}`);
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
        } else {
            emulateUserMessage.hide();
            $.cookie(cookieName, cookieVal, { expires: getExpireDate(), path: '/' });
            location.reload();
        }
    }

    function handleEmulateUserStopButtonClicked() {
        $.removeCookie(EMULATE_USER_ID, { path: '/'});
        $.removeCookie(EMULATE_USERNAME, { path: '/'});
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

    function setDjangoFlashMessageToSlide() {
        // If Django messaging is enabled, this will make the message slide up after 5 seconds
        var FADE_DURATION = 5000; // 5 seconds
        var ANIMATION_DURATION = 500 // 0.5 seconds
        $('.alert.flash-message').fadeTo(FADE_DURATION, 1).slideUp(ANIMATION_DURATION, function(){
            $('.alert.flash-message').remove();
        });
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
        setDjangoFlashMessageToSlide();
    }

    initEventHandlers();
    init();
});
