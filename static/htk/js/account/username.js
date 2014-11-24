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

    // username
    var CSS_ID_INPUT_USERNAME = 'input#id_username';
    var CSS_CLASS_USERNAME_CHANGE = 'username-change';
    var CSS_CLASS_USERNAME_FORM_CONTAINER = 'username-form-container';
    var CSS_CLASS_USERNAME_MESSAGE_CONTAINER = 'username-message-container';
    var CSS_CLASS_CURRENT_USERNAME_CONTAINER = 'current-username-container';

    var CSS_ID_PAGE_ACCOUNT_SETTINGS = 'page_account_settings';
    var CSS_ID_USERNAME_CHANGE_FORM_TEMPLATE = 'username_change_form_template';

    // ----------
    // Nodes
    var main = Y.one('#main');
    var settings = main.one('#' + CSS_ID_PAGE_ACCOUNT_SETTINGS);
    // username
    var currentUsernameContainer = settings.one('.' + CSS_CLASS_CURRENT_USERNAME_CONTAINER);
    var usernameFormContainer = settings.one('.' + CSS_CLASS_USERNAME_FORM_CONTAINER);
    var usernameMessageContainer = settings.one('.' + CSS_CLASS_USERNAME_MESSAGE_CONTAINER);
    var usernameFormTemplate = settings.one('#' + CSS_ID_USERNAME_CHANGE_FORM_TEMPLATE);

    // App variables
    var SETTINGS_FIELD_CACHE = {};
    var IO_TRANSACTION_DATA = {};

    var S_CHANGE_USERNAME_SUCCESS_MESSAGE = 'Username changed successfully.';
    var S_CHANGE_USERNAME_ERROR_MESSAGE = 'An error occurred while trying to change the username.';

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions

    function handleEnterKeyPressed(e) {
        e.preventDefault();
    }

    // --------------------------------------------------
    // Change Username Functions

    function showUsernameForm() {
        var usernameForm = Y.Node.create(usernameFormTemplate.getHTML());
        usernameForm.one(CSS_ID_INPUT_USERNAME).set('value', '');
        usernameFormContainer.setHTML(usernameForm);
    }

    function hideUsernameForm() {
        usernameFormContainer.setHTML();
    }

    function displayChangeUsernameSuccessMessage() {
        usernameMessageContainer.addClass(CSS_CLASS_UPDATE_SUCCESS);
        usernameMessageContainer.removeClass(CSS_CLASS_UPDATE_ERROR);
        usernameMessageContainer.setHTML(S_CHANGE_USERNAME_SUCCESS_MESSAGE);
    }

    function displayChangeUsernameErrorMessage(error) {
        usernameMessageContainer.addClass(CSS_CLASS_UPDATE_ERROR);
        usernameMessageContainer.removeClass(CSS_CLASS_UPDATE_SUCCESS);
        var errorMessage = S_CHANGE_USERNAME_ERROR_MESSAGE;
        if (typeof(error) !== 'undefined') {
            errorMessage += ' ' + error;
        }
        usernameMessageContainer.setHTML(errorMessage);
    }

    function clearUsernameMessage() {
        usernameMessageContainer.setHTML();
    }

    function submitUsernameForm() {
        var usernameForm = usernameFormContainer.one('form');
        var uri = usernameForm.get('action');
        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: null,
            headers: {
                'X-CSRFToken': csrftoken
            },
            form: {
                id: usernameForm,
                useDisabled: false
            },
            on: {
                complete: handleChangeUsernameResponse
            }
        }
        var username = usernameForm.one(CSS_ID_INPUT_USERNAME).get('value');
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri,
            username: username
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleChangeUsernameResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Update Username API Call');
        }
        if (responseData) {
            var status = responseData['status'];
            if (status === 'okay') {
                hideUsernameForm();
                var transactionData = IO_TRANSACTION_DATA[transactionId];
                var username = transactionData['username'];
                currentUsernameContainer.setHTML(username);
                displayChangeUsernameSuccessMessage();
            } else if (status === 'error') {
                var error = responseData['error'];
                displayChangeUsernameErrorMessage(error);
            } else {
                // impossible case, do nothing
            }
        }
    }

    function handleChangeUsernamePressed(e) {
        showUsernameForm();
        clearUsernameMessage();
    }

    function handleChangeUsernameSubmitPressed(e) {
        submitUsernameForm();
    }

    function handleChangeUsernameCancelPressed(e) {
        hideUsernameForm();
        clearUsernameMessage();
    }

    // App Initializers
    function initEventHandlers() {
        if (settings) {
            // settings field forms
            settings.delegate('key', handleEnterKeyPressed, 'down:enter', 'input');
            // username
            settings.delegate('tap', handleChangeUsernamePressed, 'a.' + CSS_CLASS_USERNAME_CHANGE);
            settings.delegate('tap', handleChangeUsernameSubmitPressed, '.' + CSS_CLASS_USERNAME_FORM_CONTAINER + ' a.' + CSS_CLASS_SUBMIT_BUTTON);
            settings.delegate('tap', handleChangeUsernameCancelPressed, '.' + CSS_CLASS_USERNAME_FORM_CONTAINER + ' a.' + CSS_CLASS_CANCEL_BUTTON);
        }
    }

    function init() {
    }
    initEventHandlers();
    init();
});
