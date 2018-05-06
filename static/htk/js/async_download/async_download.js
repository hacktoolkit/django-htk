$(function() {
    var CHECK_DELAY = 1500;

    function handleResultReady() {
        $(elt).find('.async-download-loading').hide();
        $(elt).find('.async-download-ready').removeClass('hidden');
    }

    function makeCheckUrl(url, elt) {
        var fn = function() {
            var resultStatusUrl = url + '?ping=1';
            $.get(resultStatusUrl).done(function(data) {
                if (data.ready) {
                    handleResultReady(elt);
                } else {
                    // not ready yet, check again after CHECK_DELAY
                    setTimeout(makeCheckUrl(url, elt), CHECK_DELAY);
                }
            });
        };
        return fn;
    }

    var interval = null;
    var elt = $('.async-download');
    if (elt.length) {
        var resultUrl = elt.attr('data:result-url');
        var callback = makeCheckUrl(resultUrl, elt);
        callback();
    }
});
