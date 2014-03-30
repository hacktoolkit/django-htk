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

    var CSS_CLASS_SETTINGS_FIELD_FORM = 'settings-field-form';
    // password
    var CSS_CLASS_PASSWORD_CHANGE = 'password-change';
    var CSS_CLASS_PASSWORD_FORM_CONTAINER = 'password-form-container';
    var CSS_CLASS_PASSWORD_MESSAGE_CONTAINER = 'password-message-container';
    var CSS_CLASS_SETTINGS_AVATAR = 'settings-avatar';
    var CSS_CLASS_SETTINGS_AVATAR_BOX = 'settings-avatar-box';
    // emails
    var CSS_CLASS_EMAILS_LIST = 'emails-list';
    var CSS_CLASS_EMAIL_ROW = 'email-row';
    var CSS_CLASS_ADD_EMAIL_FORM_CONTAINER = 'add-email-form-container';
    // avatar
    var CSS_CLASS_AVATAR_TYPE = 'avatar-type';

    var CSS_ID_PAGE_ACCOUNT_SETTINGS = 'page_account_settings';
    var CSS_ID_PASSWORD_CHANGE_FORM_TEMPLATE = 'password_change_form_template';
    var CSS_ID_EMAIL_ROW_TEMPLATE = 'email_row_template';

    // ----------
    // Nodes
    var main = Y.one('#main');
    var settings = main.one('#' + CSS_ID_PAGE_ACCOUNT_SETTINGS);
    // password
    var passwordFormContainer = settings.one('.' + CSS_CLASS_PASSWORD_FORM_CONTAINER);
    var passwordMessageContainer = settings.one('.' + CSS_CLASS_PASSWORD_MESSAGE_CONTAINER);
    var passwordFormTemplate = settings.one('#' + CSS_ID_PASSWORD_CHANGE_FORM_TEMPLATE);
    // emails
    var emailsList = settings.one('.' + CSS_CLASS_EMAILS_LIST);
    var addEmailFormContainer = settings.one('.' + CSS_CLASS_ADD_EMAIL_FORM_CONTAINER);
    // avatar
    var settingsAvatar = main.one('.' + CSS_CLASS_SETTINGS_AVATAR);

    // App variables
    var SETTINGS_FIELD_CACHE = {};
    var IO_TRANSACTION_DATA = {};
    var URI_SET_AVATAR = '/api/account/avatar';
    var S_CONFIRM_DELETE_EMAIL = 'Are you sure you want to delete this email address, ';

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions
    function resetFieldUpdateMessages() {
        var successMessages = Y.all('.' + CSS_CLASS_UPDATE_SUCCESS);
        successMessages.each(function(node) {
            node.removeClass('hidden');
            node.hide();
        });
        var errorMessages = Y.all('.' + CSS_CLASS_UPDATE_ERROR);
        errorMessages.each(function(node) {
            var message = node.one('.' + CSS_CLASS_MESSAGE);
            if (message) {
                message.setHTML('');
            }
            node.removeClass('hidden');
            node.hide();
        });
    }

    function saveUserSettingsField(field) {
        var form = field.ancestor('form');
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
                complete: handleUserSettingsEditResponse
            }
        }
        var request = Y.io(uri, cfg);
        var transactionId = request.id;
        var transactionData = {
            uri: uri,
            field: field
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleUserSettingsEditResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Update User Settings API Call');
        }
        if (responseData) {
            var status = responseData['status'];
            var transactionData = IO_TRANSACTION_DATA[transactionId];
            var field = transactionData.field;
            var fieldName = field.getAttribute('name');
            var form = field.ancestor('form');
            var successMessage = form.one('.' + CSS_CLASS_UPDATE_SUCCESS);
            var errorMessage = form.one('.' + CSS_CLASS_UPDATE_ERROR);
            resetFieldUpdateMessages()
            if (status === 'okay') {
                form.setStyle('opacity', '1');
                successMessage.show();
            } else {
                var fieldErrors = responseData['field_errors'];
                var fieldErrorMessage = fieldErrors[fieldName];
                errorMessage.show();
                errorMessage.one('.' + CSS_CLASS_MESSAGE).setHTML(fieldErrorMessage);
            }
        }
    }

    function handleSettingsFieldFocused(e) {
        var field = this;
        var fieldId = field.get('id');
        var fieldValue = field.get('value');
        SETTINGS_FIELD_CACHE[fieldId] = fieldValue;
    }

    function handleSettingsFieldBlurred(e) {
        var field = this;
        var fieldId = field.get('id');
        var fieldValue = field.get('value');
        if (SETTINGS_FIELD_CACHE[fieldId] !== fieldValue) {
            var form = field.ancestor('form');
            form.setStyle('opacity', '0.5');
            saveUserSettingsField(field);
        }
    }

    function handleSettingsFieldChanged(e) {
        Y.log('asdfasdfsf');
        var field = this;
        var fieldId = field.get('id');
        var fieldValue = field.get('value');
        Y.log('fieldValue: ' + fieldValue);
        if (typeof(fieldValue) === 'undefined' || SETTINGS_FIELD_CACHE[fieldId] !== fieldValue) {
            Y.log('saving changes');
            var form = field.ancestor('form');
            form.setStyle('opacity', '0.5');
            saveUserSettingsField(field);
        }
    }

    function handleEnterKeyPressed(e) {
        e.preventDefault();
    }

    function handleAvatarSelected(e) {
        var clickedAvatar = this;

        // visual update
        var avatars = settingsAvatar.all('.' + CSS_CLASS_SETTINGS_AVATAR_BOX);
        avatars.each(function (node) {
            if (node === clickedAvatar) {
                node.removeClass(CSS_CLASS_DESELECTED);
            } else {
                node.addClass(CSS_CLASS_DESELECTED);
            }
        });

        // build request payload
        var avatarType = clickedAvatar.one('.' + CSS_CLASS_AVATAR_TYPE);
        var avatarTypeValue = avatarType.get('text').trim().toUpperCase();

        var data = {
            'type' : avatarTypeValue
        };

        var csrftoken = Y.Cookie.get('csrftoken');
        var cfg = {
            method: 'POST',
            data: Y.JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        };
        Y.io(URI_SET_AVATAR, cfg);
    }

    // --------------------------------------------------
    // Change Password Functions

    function showPasswordForm() {
        passwordFormContainer.setHTML(passwordFormTemplate.getHTML());
    }

    function hidePasswordForm() {
        passwordFormContainer.setHTML();
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
            uri: uri,
        };
        IO_TRANSACTION_DATA[transactionId] = transactionData;
    }

    function handleChangePasswordResponse(transactionId, response) {
        var responseData = null;
        try {
            responseData = Y.JSON.parse(response.responseText);
        } catch (e) {
            _rollbar.push('Bad JSON response received from Update Password API Call');
        }
        if (responseData) {
            var status = responseData['status'];
            if (status === 'okay') {
                hidePasswordForm();
                passwordMessageContainer.addClass(CSS_CLASS_UPDATE_SUCCESS);
                passwordMessageContainer.removeClass(CSS_CLASS_UPDATE_ERROR);
                passwordMessageContainer.setHTML('Password changed successfully.');
            } else if (status === 'error') {
                passwordMessageContainer.addClass(CSS_CLASS_UPDATE_ERROR);
                passwordMessageContainer.removeClass(CSS_CLASS_UPDATE_SUCCESS);
                passwordMessageContainer.setHTML('An error occurred while trying to change the password.');
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

    // --------------------------------------------------
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
        settings.delegate('focus', handleSettingsFieldFocused, 'form.' + CSS_CLASS_SETTINGS_FIELD_FORM + ' input' );
        settings.delegate('focus', handleSettingsFieldFocused, 'form.' + CSS_CLASS_SETTINGS_FIELD_FORM + ' textarea' );
        settings.delegate('blur', handleSettingsFieldBlurred, 'form.' + CSS_CLASS_SETTINGS_FIELD_FORM + ' input' );
        settings.delegate('blur', handleSettingsFieldBlurred, 'form.' + CSS_CLASS_SETTINGS_FIELD_FORM + ' textarea' );
        settings.delegate('change', handleSettingsFieldChanged, 'form.' + CSS_CLASS_SETTINGS_FIELD_FORM + ' select');
//        settings.delegate('change', handleSettingsFieldChanged, 'form' + ' input');

        // password
        settings.delegate('tap', handleChangePasswordPressed, 'a.' + CSS_CLASS_PASSWORD_CHANGE);
        settings.delegate('tap', handleChangePasswordSubmitPressed, '.' + CSS_CLASS_PASSWORD_FORM_CONTAINER + ' a.' + CSS_CLASS_SUBMIT_BUTTON);
        settings.delegate('tap', handleChangePasswordCancelPressed, '.' + CSS_CLASS_PASSWORD_FORM_CONTAINER + ' a.' + CSS_CLASS_CANCEL_BUTTON);

        // emails
        settings.delegate('tap', handleAddEmailSubmitPressed, '.' + CSS_CLASS_ADD_EMAIL_FORM_CONTAINER + ' a.' + CSS_CLASS_SUBMIT_BUTTON);
        settings.delegate('tap', handleDeleteEmailPressed, '.' + CSS_CLASS_EMAIL_ROW + ' a.' + CSS_CLASS_DELETE);
        settings.delegate('tap', handleSetPrimaryEmailPressed, '.' + CSS_CLASS_EMAIL_ROW + ' a.' + CSS_CLASS_SET_PRIMARY);

        // avatar
        settingsAvatar.delegate('tap', handleAvatarSelected, '.' + CSS_CLASS_SETTINGS_AVATAR_BOX);
    }

    function init() {
        resetFieldUpdateMessages();
    }
    initEventHandlers();
    init();
});
