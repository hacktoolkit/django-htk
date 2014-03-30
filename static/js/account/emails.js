YUI().use(
    'node',
    'event',
    'cookie',
    'io',
    'json',
    'handlebars',
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
    var CSS_CLASS_DELETE = 'delete';
    var CSS_CLASS_SET_PRIMARY = 'set-primary';

    // emails
    var CSS_CLASS_EMAILS_LIST = 'emails-list';
    var CSS_CLASS_EMAIL_ROW = 'email-row';
    var CSS_CLASS_ADD_EMAIL_FORM_CONTAINER = 'add-email-form-container';

    var CSS_ID_PAGE_ACCOUNT_SETTINGS = 'page_account_settings';
    var CSS_ID_EMAIL_ROW_TEMPLATE = 'email_row_template';

    // ----------
    // Nodes
    var main = Y.one('#main');
    var settings = main.one('#' + CSS_ID_PAGE_ACCOUNT_SETTINGS);
    // emails
    var emailsList = settings.one('.' + CSS_CLASS_EMAILS_LIST);
    var addEmailFormContainer = settings.one('.' + CSS_CLASS_ADD_EMAIL_FORM_CONTAINER);

    // App variables
    var SETTINGS_FIELD_CACHE = {};
    var IO_TRANSACTION_DATA = {};

    var S_CONFIRM_DELETE_EMAIL = 'Are you sure you want to delete this email address, ';

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions
    function handleEnterKeyPressed(e) {
        e.preventDefault();
    }

    // Update Email functions

    function handleAddEmailSubmitPressed(e) {
        var button = this;
        var form = button.ancestor('form');
        var uri = form.get('action');
        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: null,
            headers: {
                'X-CSRFToken': csrftoken
            },
            form: {
                id: form,
                useDisabled: false
            },
            on: {
                complete: handleAddEmailResponse
            }
        }
        var email = form.one('input#id_email').get('value');
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri,
            form: form,
            email: email
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleAddEmailResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Add Email API Call');
        }
        if (responseData) {
            var transactionData = IO_TRANSACTION_DATA[transactionId];
            var form = transactionData['form'];
            var status = responseData['status'];
            var email = transactionData['email'];
            if (status === 'okay') {
                // reset the field values
                form.all('input').each(function(input) {
                    input.set('value', '');
                });
                displayAddedEmail(email);
                showAddEmailSuccessMessage();
            } else {
                showAddEmailErrorMessage();
            }
        }
    }

    function displayAddedEmail(email) {
        var emailRowTemplate = Y.one('#' + CSS_ID_EMAIL_ROW_TEMPLATE);
        var template = Y.Handlebars.compile(emailRowTemplate.getHTML());
        var data = {
            'email': email
        };
        var html = template(data);
        emailsList.append(html);
    }

    function showAddEmailSuccessMessage() {
        var successMessage = addEmailFormContainer.one('.' + CSS_CLASS_UPDATE_SUCCESS);
        successMessage.removeClass(CSS_CLASS_HIDDEN);
        successMessage.show();
        var errorMessage = addEmailFormContainer.one('.' + CSS_CLASS_UPDATE_ERROR);
        errorMessage.removeClass(CSS_CLASS_HIDDEN);
        errorMessage.hide();
    }

    function showAddEmailErrorMessage(form) {
        var errorMessage = addEmailFormContainer.one('.' + CSS_CLASS_UPDATE_ERROR);
        errorMessage.removeClass(CSS_CLASS_HIDDEN);
        errorMessage.show();
        var successMessage = addEmailFormContainer.one('.' + CSS_CLASS_UPDATE_SUCCESS);
        successMessage.removeClass(CSS_CLASS_HIDDEN);
        successMessage.hide();
    }

    function handleDeleteEmailPressed(e) {
        var emailField = this.previous('input');
        var email = emailField.get('value');
        if (confirm(S_CONFIRM_DELETE_EMAIL + email + '?')) {
            var form = this.ancestor('form');
            submitDeleteEmailForm(form);
        }
    }

    function submitDeleteEmailForm(form) {
        var uri = form.get('action');
        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: null,
            headers: {
                'X-CSRFToken': csrftoken
            },
            form: {
                id: form,
                useDisabled: false
            },
            on: {
                complete: handleDeleteEmailResponse
            }
        }
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri,
            form: form
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleDeleteEmailResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Delete Email API Call');
        }
        if (responseData) {
            var transactionData = IO_TRANSACTION_DATA[transactionId];
            var form = transactionData['form'];
            var status = responseData['status'];
            if (status === 'okay') {
                var emailRow = form.ancestor('.' + CSS_CLASS_EMAIL_ROW);
                emailRow.remove();
            } else {
            }
        }
    }

    function handleSetPrimaryEmailPressed(e) {
        var button = this;
        var form = button.ancestor('form');
        var uri = form.get('action');
        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: null,
            headers: {
                'X-CSRFToken': csrftoken
            },
            form: {
                id: form,
                useDisabled: false
            },
            on: {
                complete: handleSetPrimaryEmailResponse
            }
        }
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri,
            form: form
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleSetPrimaryEmailResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Set Primary Email API Call');
        }
        if (responseData) {
            var transactionData = IO_TRANSACTION_DATA[transactionId];
            var form = transactionData['form'];
            var status = responseData['status'];
            if (status === 'okay') {
                // TODO: update inline without refreshing
                location.reload();
            } else {
            }
        }
    }

    // App Initializers
    function initEventHandlers() {
        // settings field forms
        settings.delegate('key', handleEnterKeyPressed, 'down:enter', 'input');
        // emails
        settings.delegate('tap', handleAddEmailSubmitPressed, '.' + CSS_CLASS_ADD_EMAIL_FORM_CONTAINER + ' a.' + CSS_CLASS_SUBMIT_BUTTON);
        settings.delegate('tap', handleDeleteEmailPressed, '.' + CSS_CLASS_EMAIL_ROW + ' a.' + CSS_CLASS_DELETE);
        settings.delegate('tap', handleSetPrimaryEmailPressed, '.' + CSS_CLASS_EMAIL_ROW + ' a.' + CSS_CLASS_SET_PRIMARY);
    }

    function init() {
    }
    initEventHandlers();
    init();
});
