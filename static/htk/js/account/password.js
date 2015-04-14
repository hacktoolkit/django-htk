var REQUIRE_PASSWORD_FUNCTION = null;

YUI().use(
    'node',
    'event',
    'cookie',
    'io',
    'json',
function (Y) {
    /* -------------------------------------------------- */
    /* YUI "Local" Globals */

    // CSS selectors
    var CSS_CLASS_HIDDEN = 'hidden';
    var CSS_CLASS_VISIBLE = 'visible';
    var CSS_CLASS_UPDATE_SUCCESS = 'update-success';
    var CSS_CLASS_UPDATE_ERROR = 'update-error';
    var CSS_CLASS_DESELECTED = 'deselected';
    var CSS_CLASS_MESSAGE = 'message';
    var CSS_CLASS_SUBMIT_BUTTON = 'submit-button';
    var CSS_CLASS_CANCEL_BUTTON = 'cancel-button';
    var CSS_CLASS_SET_PRIMARY = 'set-primary';

    // password
    var CSS_CLASS_PASSWORD_CHANGE = 'password-change';
    var CSS_CLASS_PASSWORD_FORM_CONTAINER = 'password-form-container';
    var CSS_CLASS_PASSWORD_MESSAGE_CONTAINER = 'password-message-container';

    var CSS_ID_PAGE_ACCOUNT_SETTINGS = 'page_account_settings';
    var CSS_ID_PASSWORD_CHANGE_FORM_TEMPLATE = 'password_change_form_template';

    // ----------
    // Nodes
    var main = Y.one('#main');
    var settings = main.one('#' + CSS_ID_PAGE_ACCOUNT_SETTINGS);
    // password
    var passwordFormContainer = settings.one('.' + CSS_CLASS_PASSWORD_FORM_CONTAINER);
    var passwordMessageContainer = settings.one('.' + CSS_CLASS_PASSWORD_MESSAGE_CONTAINER);
    var passwordFormTemplate = settings.one('#' + CSS_ID_PASSWORD_CHANGE_FORM_TEMPLATE);

    // App variables
    var SETTINGS_FIELD_CACHE = {};
    var IO_TRANSACTION_DATA = {};

    var S_PASSWORD_REQUIRED_MESSAGE = 'Please set a password to complete your account settings.';
    var S_CHANGE_PASSWORD_SUCCESS_MESSAGE = 'Password changed successfully.';
    var S_CHANGE_PASSWORD_ERROR_MESSAGE = 'An error occurred while trying to change the password.';

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions

    function handleEnterKeyPressed(e) {
        e.preventDefault();
    }

    // --------------------------------------------------
    // Change Password Functions

    function showPasswordForm() {
        passwordFormContainer.setHTML(passwordFormTemplate.getHTML());
    }

    function requirePassword(focus) {
        showPasswordForm();
        passwordMessageContainer.setHTML(S_PASSWORD_REQUIRED_MESSAGE);
        if (focus) {
            var input = passwordFormContainer.one('.pure-input-1');
            input.focus();
        }
    }
    REQUIRE_PASSWORD_FUNCTION = requirePassword;

    function hidePasswordForm() {
        passwordFormContainer.setHTML();
    }

    function displayChangePasswordSuccessMessage() {
        passwordMessageContainer.addClass(CSS_CLASS_UPDATE_SUCCESS);
        passwordMessageContainer.removeClass(CSS_CLASS_UPDATE_ERROR);
        passwordMessageContainer.setHTML(S_CHANGE_PASSWORD_SUCCESS_MESSAGE);
    }

    function displayChangePasswordErrorMessage() {
        passwordMessageContainer.addClass(CSS_CLASS_UPDATE_ERROR);
        passwordMessageContainer.removeClass(CSS_CLASS_UPDATE_SUCCESS);
        passwordMessageContainer.setHTML(S_CHANGE_PASSWORD_ERROR_MESSAGE);
    }

    function clearPasswordMessage() {
        passwordMessageContainer.setHTML();
    }

    function submitPasswordForm() {
        var passwordForm = passwordFormContainer.one('form');
        var uri = passwordForm.get('action');
        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: null,
            headers: {
                'X-CSRFToken': csrftoken
            },
            form: {
                id: passwordForm,
                useDisabled: false
            },
            on: {
                complete: handleChangePasswordResponse
            }
        }
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleChangePasswordResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            Rollbar.error('Bad JSON response received from Update Password API Call');
        }
        if (responseData) {
            var status = responseData['status'];
            if (status === 'okay') {
                hidePasswordForm();
                displayChangePasswordSuccessMessage();
                HAS_PASSWORD_SET = true;
            } else if (status === 'error') {
                displayChangePasswordErrorMessage();
            } else {
                // impossible case, do nothing
            }
        }
    }

    function handleChangePasswordPressed(e) {
        showPasswordForm();
        clearPasswordMessage();
    }

    function handleChangePasswordSubmitPressed(e) {
        submitPasswordForm();
    }

    function handleChangePasswordCancelPressed(e) {
        hidePasswordForm();
        clearPasswordMessage();
    }

    // App Initializers
    function initEventHandlers() {
        if (settings) {
            // settings field forms
            settings.delegate('key', handleEnterKeyPressed, 'down:enter', 'input');
            // password
            settings.delegate('tap', handleChangePasswordPressed, 'a.' + CSS_CLASS_PASSWORD_CHANGE);
            settings.delegate('tap', handleChangePasswordSubmitPressed, '.' + CSS_CLASS_PASSWORD_FORM_CONTAINER + ' a.' + CSS_CLASS_SUBMIT_BUTTON);
            settings.delegate('tap', handleChangePasswordCancelPressed, '.' + CSS_CLASS_PASSWORD_FORM_CONTAINER + ' a.' + CSS_CLASS_CANCEL_BUTTON);
        }
    }

    function init() {
        if (PASSWORD_REQUIRED && !HAS_PASSWORD_SET) {
            requirePassword();
        }
    }
    initEventHandlers();
    init();
});
