$(function() {
    var CHECK_DELAY = 1500;

    function handleResultRunning() {
        $(elt).find('.async-task-status-pending').hide();
        $(elt).find('.async-task-status-ready').removeClass('hidden').hide();

        $(elt).find('.async-task-status-running').removeClass('hidden').show();
    }

    function handleResultReady() {
        $(elt).find('.async-task-status-pending').hide();
        $(elt).find('.async-task-status-running').removeClass('hidden').hide();

        $(elt).find('.async-task-status-ready').removeClass('hidden').show();
    }

    function makeCheckUrl(url, elt) {
        var fn = function() {
            $.get(url).done(function(data) {
                if (data.ready) {
                    handleResultReady(elt);
                } else {
                    if (data.state === 'STARTED') {
                        handleResultRunning(elt);
                    }
                    // not ready yet, check again after CHECK_DELAY
                    setTimeout(makeCheckUrl(url, elt), CHECK_DELAY);
                }
            });
        };
        return fn;
    }

    var interval = null;
    var elt = $('.async-task');
    if (elt.length) {
        var resultUrl = elt.attr('data:result-status-url');
        var callback = makeCheckUrl(resultUrl, elt);
        callback();
    }
});
