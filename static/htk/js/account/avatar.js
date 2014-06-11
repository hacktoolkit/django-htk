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

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions

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
        // avatar
        if (settingsAvatar) {
            settingsAvatar.delegate('tap', handleAvatarSelected, '.' + CSS_CLASS_SETTINGS_AVATAR_BOX);
        }
    }

    function init() {
    }
    initEventHandlers();
    init();
});
