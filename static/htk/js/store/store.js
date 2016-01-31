$(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = $.cookie('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    function handleProductClicked(e) {
        var target = $(e.currentTarget);
        var productTile = target.parents('.product-tile');
        var productUri = $(productTile).attr('data:uri');
        // TODO: open a overlay window
        // TODO: capture modifier keys to open in new window
        // TODO: url history manipulation
        window.location = productUri;
    }

    function initEventHandlers() {
        $('.product-tile .hover-container').click(handleProductClicked);
    }

    function init() {
    }

    initEventHandlers();
    init();
});
