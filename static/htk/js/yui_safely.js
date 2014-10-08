// Checks for the presence of YUI.
// If it doesn't exist, meaning YUI didn't load properly, reload the page.

var P_YUI_RELOAD = 'yui_reload';

if (typeof(YUI) === 'undefined') {
    if (typeof(YUI_RELOAD_ATTEMPTS) === 'number' && YUI_RELOAD_ATTEMPTS < YUI_RELOAD_MAX_ATTEMPTS) {
        Rollbar.info('YUI is undefined. Attempting to reload');
        var url = document.location.href;
        var params = document.location.search;
        var paramJoinChar = '';
        var reloadUrl = url;
        var reloadParam = P_YUI_RELOAD + '=1';
        if (url.indexOf(P_YUI_RELOAD) > 0) {
            // this is already a reload, just force reload
            document.location.reload(true);
        } else if (params == '') {
            reloadUrl += '?' + reloadParam;
        } else {
            reloadUrl += '&' + reloadParam;
        }
        document.location.href = reloadUrl;
    }
} else {
    // do nothing
}

// if we're still running at this point, manipulate the history to get rid of yui_reload from the params
var _safe_params = document.location.search;
if (_safe_params.indexOf(P_YUI_RELOAD) > 0) {
    var params = _safe_params.substring(1).split('&');
    var cleanedParams = [];
    for (var i=0; i < params.length; ++i ) {
        var param = params[i];
        if (param.indexOf(P_YUI_RELOAD) >= 0) {
            // ignore this, don't copy it over
        } else {
            cleanedParams.push(param)
        }
    }
    var cleanedParamString = '';
    if (cleanedParams.length > 0) {
        cleanedParamString = '?' + cleanedParams.join('&');
    } else {
        // do nothing
    }
    var prettyUrl = document.location.origin + document.location.pathname + cleanedParamString;
    window.history.replaceState({}, '', prettyUrl);
}
