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
    var CSS_CLASS_DELETE = 'delete';
    var CSS_CLASS_SET_PRIMARY = 'set-primary';

    var CSS_CLASS_SETTINGS_FIELD_FORM = 'settings-field-form';

    // avatar
    var CSS_CLASS_AVATAR_TYPE = 'avatar-type';
    var CSS_CLASS_SETTINGS_AVATAR = 'settings-avatar';
    var CSS_CLASS_SETTINGS_AVATAR_BOX = 'settings-avatar-box';

    var CSS_ID_PAGE_ACCOUNT_SETTINGS = 'page_account_settings';

    // ----------
    // Nodes
    var main = Y.one('#main');
    var settings = main.one('#' + CSS_ID_PAGE_ACCOUNT_SETTINGS);
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

        // avatar
        settingsAvatar.delegate('tap', handleAvatarSelected, '.' + CSS_CLASS_SETTINGS_AVATAR_BOX);
    }

    function init() {
        resetFieldUpdateMessages();
    }
    initEventHandlers();
    init();
});
