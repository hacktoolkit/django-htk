YUI().add(
    'htk-user-autocomplete',
function(Y) {

    // --------------------------------------------------
    // Internal functions

    function userAutoCompleteResultListLocator(response) {
        var results = (response && response.data && response.data.results) || [];
        return results;
    };

    function userAutoCompleteFilterHasUsernameAndName(query, results) {
        // Iterate through the array of results and return a filtered
        // array containing only results that have a non-empty username and name
        return Y.Array.filter(results, function(result) {
            var user = result.raw
            var hasUsernameAndName = Y.Lang.trim(user.username) !== '' && Y.Lang.trim(user.first_name + ' ' + user.last_name) !== '';
            return hasUsernameAndName;
        });
    };

    var userAutoCompleteResultTemplate = '{display_name} ({username})';

    function userAutoCompleteResultFormatter(query, results) {
        // Iterate over the array of result objects and return an
        // array of HTML strings
        return Y.Array.map(results, function(result) {
            var user = result.raw;
            // user is an object with keys:
            // username
            // first_name
            // last_name
            // display_name
            // gravatar_hash

            // Use string substitution to fill out the User template and
            // return an HTML string for this result
            return Y.Lang.sub(userAutoCompleteResultTemplate, user);
        });
    }

    function userAutoCompleteResultHighlighter(query, results) {
        return Y.Array.map(results, function(result) {
            var user = result.raw;
            var formatted = Y.Lang.sub(userAutoCompleteResultTemplate, user);
            var highlighted = Y.Highlight.all(formatted, query);
            return highlighted;
        });
    }
    // --------------------------------------------------
    // Public functions

    function init(node, source) {
        node.plug(Y.Plugin.AutoComplete, {
            minQueryLength: 1,
            queryDelay: 300,
            resultFilters: [userAutoCompleteFilterHasUsernameAndName],
//            resultFormatter: userAutoCompleteResultFormatter,
//            resultHighlighter: 'phraseMatch',
            resultHighlighter: userAutoCompleteResultHighlighter,
            resultListLocator: userAutoCompleteResultListLocator,
            resultTextLocator: 'username',
            source: source
        });
    }

    Y.UserAutoComplete = {
        init : init
    }

}, '0.1.0', {
    requires: [
        'node',
        'event',
        'autocomplete',
        'autocomplete-highlighters',
        'highlight'
    ]
});
