YUI().use(
    'node',
    'event',
    'event-key',
    'panel',
    'transition',
    'dd-plugin',
    'io',
    'cookie',
function(Y) {
    /* -------------------------------------------------- */
    /* YUI "Local" Globals */

    // Nodes
    var main = Y.one('#main');

    // CSS selectors
    var CSS_ID_FEEDBACK_FORM = '#feedback_form';
    var CSS_ID_FEEDBACK_PANEL = '#feedback_panel';
    var CSS_ID_FEEDBACK_TAB = '#feedback_tab';
    var CSS_ID_FEEDBACK_BUTTON = '#feedback_button';
    var CSS_ID_FEEDBACK_MAILTO = '#feedback_mailto';
    var CSS_ID_FEEDBACK_PANEL_CONTENT = '#feedback_panel_content';
    var CSS_ID_FEEDBACK_SUBMIT_BUTTON = 'button#feedback_submit';

    var CSS_CLASS_FEEDBACK_CLOSE_BUTTON = '.yui3-button-close';
    var CSS_CLASS_FEEDBACK_BUTTON = '.feedback-button';

    // App variables
    var _FEEDBACK_PANEL = null;
    var FEEDBACK_PANEL_WIDTH = 500;
    var FEEDBACK_PANEL_ZINDEX = 100;

    /* End YUI "Local" Globals */
    /* -------------------------------------------------- */

    // Custom App Functions
    function getFeedbackPanel(init) {
        init = (typeof init === 'undefined') ? true : false;
        var panelObj = null;
        if (!_FEEDBACK_PANEL && init) {
            var panel = new Y.Panel({
                //srcNode : node,
                id : 'feedback_panel',
                headerContent : 'Give feedback',
                width   : FEEDBACK_PANEL_WIDTH,
                zIndex  : FEEDBACK_PANEL_ZINDEX,
                constrain : 'body',
                centered: true,
                modal   : true,
                visible : false,
                plugins : [Y.Plugin.Drag],
                render  : true,
                buttons : [
                    // overwrite default close button to hook in our events
                    {
                        value: 'Close',
                        action: hideFeedbackPanel,
                        section: Y.WidgetStdMod.HEADER,
                        classNames: ['yui3-widget-button', 'yui3-button-close']
                    }
                ],
                hideOn: [
                    /*
                    {
                        // When we don't specify a `node`,
                        // it defaults to the `boundingBox` of this Panel instance.
                        eventName: 'clickoutside'
                    },
                    {
                        node: 'document',
                        eventName: 'key',
                        keyCode: 'esc'
                    }
                    */
                ]
            });

            // clear content from node
            panel.after('visibleChange', function(e) {
                if (e.newVal) { // panel is visible
                    var bodyContent = Y.one(CSS_ID_FEEDBACK_PANEL_CONTENT).getHTML();

                    panel.set('bodyContent', bodyContent);
                    panel.centered();

                } else {
                    panel.set('bodyContent', '');
                    //Y.later(0, this, this.destroy);
                }
            });
            _FEEDBACK_PANEL = panel;
	}

        return _FEEDBACK_PANEL;
    }

    function showFeedbackPanel() {
        var panel = getFeedbackPanel();
        if (!panel.get('visible')) {
            var bb = panel.get('boundingBox');
            bb.setStyle('opacity', 0);
            panel.show();
            bb.transition({
                duration: 0.3,
                opacity: 1
            });
        }
    }

    function hideFeedbackPanel() {
        var panel = getFeedbackPanel(false);

        if (panel) {
            var bb = panel.get('boundingBox');
            bb.transition({
                duration: 0.3,
                opacity: 0
            }, function() {
                panel.hide();
            });
        }
    }

    function submitFeedback() {
        var form = Y.one(CSS_ID_FEEDBACK_FORM);
        var csrftoken = Y.Cookie.get('csrftoken');
	var config = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                antispam: 'n' + 'o' + 't' + 'a' + 'b' + 'o' + 't'
            },
	    form: {
                id: form,
		useDisabled: false 
            },
            on: {
                complete: handleFeedbackSubmitted,
                failure: handleFeedbackSubmitted
            }
	};
	var uri = form.get('action');
	var request = Y.io(uri, config);
    }

    function handleFeedbackSubmitted() {
	hideFeedbackPanel();
    }

    function handleFeedbackButtonClicked(e) {
        e.preventDefault();
        showFeedbackPanel();
    }

    function handleFeedbackPanelEnterKeyPressed(e) {
        var panel = this;
        var target = e.target;
        var targetTag = target.get('tagName');
        if (targetTag === 'INPUT') {
            // stop propagation of enter key to prevent accidental submission
            e.halt();
        }

        return false;
    }

    function handleFeedbackPanelSubmitButton(e) {
        // stop propagation of submit button
        e.halt();
        submitFeedback();
        return false; 
    }

    // App Initializers
    function initEventHandlers() {
        Y.delegate('click', handleFeedbackButtonClicked, CSS_ID_FEEDBACK_TAB, CSS_ID_FEEDBACK_BUTTON);
        Y.delegate('click', handleFeedbackButtonClicked, 'body', CSS_ID_FEEDBACK_MAILTO);
        Y.delegate('click', handleFeedbackButtonClicked, 'body', CSS_CLASS_FEEDBACK_BUTTON);
        // --------------------------------------------------
        // inside the panel
        // submit button
        Y.delegate('key', handleFeedbackPanelSubmitButton, CSS_ID_FEEDBACK_PANEL, 'down:enter', CSS_ID_FEEDBACK_SUBMIT_BUTTON);
        Y.delegate('click', handleFeedbackPanelSubmitButton, CSS_ID_FEEDBACK_PANEL, CSS_ID_FEEDBACK_SUBMIT_BUTTON);
        // close button
        Y.one('document').delegate('key', hideFeedbackPanel, 'down:esc', CSS_ID_FEEDBACK_PANEL);
        // enter key
	Y.one('document').delegate('key', handleFeedbackPanelEnterKeyPressed, 'down:enter', CSS_ID_FEEDBACK_PANEL);
    }

    function init() {
    }
    initEventHandlers();
    init();
});
