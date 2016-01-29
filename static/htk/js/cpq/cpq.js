$(function() {
    var CPQ_TOTAL = 0;

    // String.prototype.format
    // http://stackoverflow.com/a/4673436/865091
    // First, checks if it isn't implemented yet.
    if (!String.prototype.format) {
        String.prototype.format = function() {
            var args = arguments;
            return this.replace(/{(\d+)}/g, function(match, number) { 
                return typeof args[number] != 'undefined'
                    ? args[number]
                    : match
                ;
            });
        };
    }

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

    function handlePDFButton() {
        window.open('?pdf=1');
    }

    function handlePrintButton() {
        window.print();
    }

    function formatCurrency(total) {
        var neg = false;
        if (total < 0) {
            neg = true;
            total = Math.abs(total);
        }
        return (neg ? "-$" : '$') + parseFloat(total, 10).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").toString();
    }

    function handleCPQFormCheckboxChanged(e) {
        var subtotal = 0;
        var lineItemIds = [];
        var approvedCheckboxes = $('.cpq-form input.approve:checkbox:checked');
        _.each(approvedCheckboxes, function(checkbox) {
            var value = parseFloat($(checkbox).attr('data:value'));
            subtotal += value;
            var lineItemId = $(checkbox).val();
            lineItemIds.push(lineItemId)
        });
        CPQ_TOTAL = subtotal;
        $('.stripe-pay-button').attr('data:amount', parseInt(CPQ_TOTAL * 100));
        $('.stripe-pay-button').attr('data:line_item_ids', lineItemIds.join(','));
        $('.cpq-approval-amount').html(formatCurrency(CPQ_TOTAL));
        updateApproveAndPayButtonState();
    }

    function updateApproveAndPayButtonState() {
        if ($('.cpq-approval:checkbox:checked').length > 0 && CPQ_TOTAL > 0) {
            $('.stripe-pay-button').removeClass('pure-button-disabled');
        } else {
            $('.stripe-pay-button').addClass('pure-button-disabled');
        }
    }

    function handleStripePayButton(e) {
        var target = e.target;
        e.preventDefault();
        var amount = $(target).attr('data:amount');
        var formattedAmount = formatCurrency(parseInt(amount) / 100);
        var lineItemIds = $(target).attr('data:line_item_ids');
        var numItems = lineItemIds.split(',').length;
        var description = '{0} item{1} ({2})'.format(numItems, (numItems > 1? 's' : ''), formattedAmount);
        var handler = StripeCheckout.configure({
            key: STRIPE_KEY,
            image: GRAVATAR_IMG,
            token: createTransactionProcessorCallback(amount, lineItemIds)
        });
        handler.open({
            name: STRIPE_CHECKOUT_NAME,
            description: description,
            amount: amount,
            panelLabel: 'Pay {{amount}}'
        });
    }

    /**
     * createTransactionProcessorCallback
     *
     * Creates the callback function to create the charge on the server using `token`
     *
     */
    function createTransactionProcessorCallback(amount, lineItemIds) {
        var callback = function(token) {
            var uri = CPQ_PAYMENT_URI;
            var data = {
                stripeToken : token.id,
                email : token.email,
                amount : amount,
                lineItemIds : lineItemIds
            };
            $.ajax(
                uri,
                {
                    method: 'POST',
                    data: data
                }
            ).done(function(data) {
                console.log('Transaction complete');
                window.location = window.location;
            }).fail(function(data) {
                console.log('Failed to charge payment card');
            }).always(function(data) {
                // nothing for now
            });
        };
        return callback;
    }

    function initEventHandlers() {
        $('.pdf-button').click(handlePDFButton);
        $('.print-button').click(handlePrintButton);
        $('.stripe-pay-button').click(handleStripePayButton);
        $('.cpq-form input:checkbox').change(handleCPQFormCheckboxChanged);
        $('.cpq-approval:checkbox').change(updateApproveAndPayButtonState);
    }

    function init() {
    }

    initEventHandlers();
    init();
});
